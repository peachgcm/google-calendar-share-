"""
Simpler version using public iCal feed - no authentication required!
Just make your Google Calendar public and use its iCal URL.
"""
from flask import Flask, render_template, request
import requests
from icalendar import Calendar
from datetime import datetime, timedelta, date, timezone
import os
from dotenv import load_dotenv
try:
    from zoneinfo import ZoneInfo
except ImportError:
    # Fallback for Python < 3.9
    from backports.zoneinfo import ZoneInfo

load_dotenv()

app = Flask(__name__)

# Get the public iCal URL from environment variable
# You can find this in Google Calendar settings > Integrate calendar > Public URL to iCal
ICAL_URL = os.environ.get('ICAL_URL', '')
# How many days ahead to show available slots (weekdays only, 9–5 in chosen TZ)
CALENDAR_HORIZON_DAYS = int(os.environ.get('CALENDAR_HORIZON_DAYS', '90'))

# Main timezones (all 4 US time zones)
TIMEZONES = {
    'PST': 'America/Los_Angeles',
    'MST': 'America/Denver',
    'CST': 'America/Chicago',
    'EST': 'America/New_York'
}

# All timezones for multi-timezone display
ALL_TIMEZONES = {
    'PST': 'America/Los_Angeles',
    'MST': 'America/Denver',
    'CST': 'America/Chicago',
    'EST': 'America/New_York',
    'UTC': 'UTC',
    'GMT': 'Europe/London',
    'CET': 'Europe/Paris',
    'JST': 'Asia/Tokyo',
    'IST': 'Asia/Kolkata',
    'AEST': 'Australia/Sydney'
}

def _merge_intervals(intervals):
    """Merge overlapping [start, end) datetime intervals."""
    if not intervals:
        return []
    intervals = sorted(intervals, key=lambda x: x[0])
    merged = [list(intervals[0])]
    for s, e in intervals[1:]:
        if s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return [(a[0], a[1]) for a in merged]


def get_available_time_slots_by_week(url, tz_name='PST'):
    """Get available time slots grouped by week for weekdays from today through horizon."""
    if not url:
        return {}
    
    # Get timezone
    tz_str = TIMEZONES.get(tz_name, TIMEZONES['PST'])
    try:
        display_tz = ZoneInfo(tz_str)
    except Exception:
        display_tz = ZoneInfo('America/Los_Angeles')  # Default to PST
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        cal = Calendar.from_ical(response.text)
        now_utc = datetime.now(timezone.utc)
        now_tz = now_utc.astimezone(display_tz)
        
        today_date = now_tz.date()
        end_date = today_date + timedelta(days=CALENDAR_HORIZON_DAYS)
        
        # Range bounds for filtering events that could affect availability
        range_start_dt = datetime.combine(today_date, datetime.min.time()).replace(tzinfo=display_tz)
        # Exclusive upper bound: start of day after last included date
        range_end_exclusive = datetime.combine(end_date + timedelta(days=1), datetime.min.time()).replace(tzinfo=display_tz)
        
        # Working hours: 9 AM to 5 PM in display timezone
        work_start_hour = 9
        work_end_hour = 17
        
        # All timed busy intervals that overlap the planning window
        all_busy = []
        
        for component in cal.walk('vevent'):
            dtstart = component.get('dtstart')
            if not dtstart:
                continue
            
            start_dt = dtstart.dt
            if not isinstance(start_dt, datetime):
                continue
            
            if start_dt.tzinfo is None:
                start_dt = start_dt.replace(tzinfo=timezone.utc)
            start_tz = start_dt.astimezone(display_tz)
            
            dtend = component.get('dtend')
            if not dtend:
                continue
            end_dt = dtend.dt
            if not isinstance(end_dt, datetime):
                continue
            if end_dt.tzinfo is None:
                end_dt = end_dt.replace(tzinfo=timezone.utc)
            end_tz = end_dt.astimezone(display_tz)
            
            if end_tz <= range_start_dt or start_tz >= range_end_exclusive:
                continue
            all_busy.append((start_tz, end_tz))
        
        # Calculate available time slots
        available_slots = []
        min_duration_minutes = 30
        
        d = today_date
        while d <= end_date:
            if d.weekday() > 4:
                d += timedelta(days=1)
                continue
            
            work_start_naive = datetime.combine(d, datetime.min.time().replace(hour=work_start_hour))
            work_end_naive = datetime.combine(d, datetime.min.time().replace(hour=work_end_hour))
            work_start = work_start_naive.replace(tzinfo=display_tz)
            work_end = work_end_naive.replace(tzinfo=display_tz)
            
            # For today, availability starts now (not before current time)
            if d == today_date:
                current_time = max(work_start, now_tz)
            else:
                current_time = work_start
            
            if current_time >= work_end:
                d += timedelta(days=1)
                continue
            
            # Busy segments on this day, clipped to the work window
            day_busy = []
            for b_s, b_e in all_busy:
                seg_start = max(b_s, work_start)
                seg_end = min(b_e, work_end)
                if seg_end > seg_start:
                    day_busy.append((seg_start, seg_end))
            day_busy = _merge_intervals(day_busy)
            
            for busy_start, busy_end in day_busy:
                if current_time < busy_start:
                    slot_start = current_time
                    slot_end = min(busy_start, work_end)
                    
                    if slot_end > slot_start:
                        duration = slot_end - slot_start
                        duration_minutes = int(duration.total_seconds() // 60)
                        
                        if duration_minutes >= min_duration_minutes:
                            available_slots.append({
                                'date': d,
                                'start': slot_start,
                                'end': slot_end,
                                'start_dt': slot_start,
                                'weekday': d.weekday()
                            })
                
                current_time = max(current_time, busy_end)
            
            if current_time < work_end:
                duration = work_end - current_time
                duration_minutes = int(duration.total_seconds() // 60)
                
                if duration_minutes >= min_duration_minutes:
                    available_slots.append({
                        'date': d,
                        'start': current_time,
                        'end': work_end,
                        'start_dt': current_time,
                        'weekday': d.weekday()
                    })
            
            d += timedelta(days=1)
        
        # Group by week
        weeks = {}
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        
        for slot in available_slots:
            # Calculate week number (week starting Monday)
            date_obj = slot['date']
            # Get the Monday of that week
            days_since_monday = date_obj.weekday()
            week_start = date_obj - timedelta(days=days_since_monday)
            week_key = week_start.isoformat()
            
            if week_key not in weeks:
                weeks[week_key] = {
                    'week_start': week_start,
                    'days': {i: [] for i in range(5)}  # Monday to Friday
                }
            
            # Format slot with time in the selected timezone only
            duration = slot['end'] - slot['start']
            hours = int(duration.total_seconds() // 3600)
            minutes = int((duration.total_seconds() % 3600) // 60)
            
            if hours > 0 and minutes > 0:
                duration_str = f"{hours}h {minutes}m"
            elif hours > 0:
                duration_str = f"{hours}h"
            else:
                duration_str = f"{minutes}m"
            
            # Convert to display timezone (already in display_tz, just format)
            start_str = slot['start'].strftime('%I:%M %p').lstrip('0')
            end_str = slot['end'].strftime('%I:%M %p').lstrip('0')
            time_str = f"{start_str} - {end_str}"
            
            formatted_slot = {
                'date': date_obj,
                'date_str': date_obj.strftime('%B %d'),
                'time': time_str,  # Time in selected timezone only
                'duration': duration_str,
                'start_dt': slot['start_dt']
            }
            
            weeks[week_key]['days'][slot['weekday']].append(formatted_slot)
        
        # Sort weeks and days
        sorted_weeks = {}
        for week_key in sorted(weeks.keys()):
            week_data = weeks[week_key]
            # Sort slots within each day
            for day_idx in range(5):
                week_data['days'][day_idx].sort(key=lambda x: x['start_dt'])
            sorted_weeks[week_key] = week_data
        
        return sorted_weeks
    
    except Exception as e:
        print(f"Error fetching available time slots: {e}")
        import traceback
        traceback.print_exc()
        return {}

@app.route('/')
def index():
    """Display the public calendar page with available time slots grouped by week."""
    # Get timezone from request (default to PST)
    tz_name = request.args.get('tz', 'PST')
    selected_week = request.args.get('week', None)
    
    # Always fetch fresh data (no caching)
    weeks_data = get_available_time_slots_by_week(ICAL_URL, tz_name)
    
    # Get list of available weeks
    week_list = []
    for week_key in sorted(weeks_data.keys()):
        week_start = weeks_data[week_key]['week_start']
        week_end = week_start + timedelta(days=4)  # Friday
        week_list.append({
            'key': week_key,
            'label': f"{week_start.strftime('%b %d')} - {week_end.strftime('%b %d, %Y')}"
        })
    
    # If no week selected, use first week
    if not selected_week and week_list:
        selected_week = week_list[0]['key']
    
    # Get data for selected week
    selected_week_data = weeks_data.get(selected_week, {})
    
    # Prepare day dates for the selected week
    day_dates = []
    if selected_week_data and 'week_start' in selected_week_data:
        week_start = selected_week_data['week_start']
        for i in range(5):  # Monday to Friday
            day_dates.append(week_start + timedelta(days=i))
    
    response = app.make_response(render_template(
        'calendar.html',
        weeks_data=weeks_data,
        week_list=week_list,
        selected_week=selected_week,
        selected_week_data=selected_week_data,
        day_dates=day_dates,
        current_tz=tz_name,
        timezones=TIMEZONES,
        horizon_days=CALENDAR_HORIZON_DAYS,
    ))
    # Prevent caching to ensure fresh data
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    if not ICAL_URL:
        print("\n⚠️  WARNING: ICAL_URL not set!")
        print("Please set ICAL_URL in your .env file or environment variables.")
        print("You can find your calendar's public iCal URL in Google Calendar settings.")
        print("\nTo get the URL:")
        print("1. Go to Google Calendar")
        print("2. Click the three dots next to your calendar")
        print("3. Select 'Settings and sharing'")
        print("4. Scroll to 'Integrate calendar'")
        print("5. Copy the 'Public URL to iCal'")
        print("\nThen add to .env: ICAL_URL=your_url_here\n")
    
    # Get port from environment variable (for cloud services) or use default
    port = int(os.environ.get('PORT', 5001))
    # Disable debug mode in production
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
