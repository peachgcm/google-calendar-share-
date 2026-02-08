"""
Simpler version using public iCal feed - no authentication required!
Just make your Google Calendar public and use its iCal URL.
"""
from flask import Flask, render_template, request, jsonify
import requests
from icalendar import Calendar
from datetime import datetime, timedelta, date, timezone
import os
import hashlib
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

def get_calendar_hash(url):
    """Get a hash of the calendar data to detect changes."""
    if not url:
        return None
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        # Create hash of the calendar content
        return hashlib.md5(response.text.encode()).hexdigest()
    except:
        return None

def get_available_time_slots_by_week(url, tz_name='PST'):
    """Get available time slots grouped by week for weekdays in remaining February dates."""
    if not url:
        return {}
    
    # Get timezone
    tz_str = TIMEZONES.get(tz_name, TIMEZONES['PST'])
    try:
        display_tz = ZoneInfo(tz_str)
    except:
        display_tz = ZoneInfo('America/Los_Angeles')  # Default to PST
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        cal = Calendar.from_ical(response.text)
        now_utc = datetime.now(timezone.utc)
        now_tz = now_utc.astimezone(display_tz)
        
        current_year = now_tz.year
        current_month = now_tz.month
        current_day = now_tz.day
        
        # Define February end date
        if current_month == 2:
            feb_start = current_day
        else:
            feb_start = 1
        
        feb_end = 28 if current_year % 4 != 0 or (current_year % 100 == 0 and current_year % 400 != 0) else 29
        
        # Working hours: 9 AM to 5 PM in display timezone
        work_start_hour = 9
        work_end_hour = 17
        
        # Collect all busy events for February weekdays
        busy_slots = []
        
        for component in cal.walk('vevent'):
            dtstart = component.get('dtstart')
            if not dtstart:
                continue
            
            start_dt = dtstart.dt
            if not isinstance(start_dt, datetime):
                continue
            
            # Make timezone-aware
            if start_dt.tzinfo is None:
                start_dt = start_dt.replace(tzinfo=timezone.utc)
            
            # Convert to display timezone
            start_tz = start_dt.astimezone(display_tz)
            
            # Only process February dates
            if start_tz.month != 2 or start_tz.year != current_year:
                continue
            
            # Only process weekdays (Monday=0, Friday=4)
            if start_tz.weekday() > 4:
                continue
            
            # Only process remaining dates
            if start_tz.day < feb_start:
                continue
            
            # Get end time
            dtend = component.get('dtend')
            if dtend:
                end_dt = dtend.dt
                if isinstance(end_dt, datetime):
                    if end_dt.tzinfo is None:
                        end_dt = end_dt.replace(tzinfo=timezone.utc)
                    end_tz = end_dt.astimezone(display_tz)
                    busy_slots.append((start_tz, end_tz))
        
        # Group busy slots by date
        busy_by_date = {}
        for start, end in busy_slots:
            date_key = start.date()
            if date_key not in busy_by_date:
                busy_by_date[date_key] = []
            busy_by_date[date_key].append((start, end))
        
        # Sort busy slots for each date
        for date_key in busy_by_date:
            busy_by_date[date_key].sort(key=lambda x: x[0])
        
        # Calculate available time slots
        available_slots = []
        min_duration_minutes = 30
        
        # Iterate through each weekday in remaining February
        for day in range(feb_start, feb_end + 1):
            try:
                date_obj = date(current_year, 2, day)
                # Check if it's a weekday
                if date_obj.weekday() > 4:
                    continue
                
                # Create datetime objects for work hours in display timezone
                work_start_naive = datetime.combine(date_obj, datetime.min.time().replace(hour=work_start_hour))
                work_end_naive = datetime.combine(date_obj, datetime.min.time().replace(hour=work_end_hour))
                work_start = work_start_naive.replace(tzinfo=display_tz)
                work_end = work_end_naive.replace(tzinfo=display_tz)
                
                # Skip if date is in the past
                if work_start < now_tz:
                    continue
                
                # Get busy slots for this date
                busy_today = busy_by_date.get(date_obj, [])
                
                # Calculate available slots
                current_time = work_start
                
                for busy_start, busy_end in busy_today:
                    if current_time < busy_start:
                        slot_start = current_time
                        slot_end = min(busy_start, work_end)
                        
                        if slot_end > slot_start:
                            duration = slot_end - slot_start
                            duration_minutes = int(duration.total_seconds() // 60)
                            
                            if duration_minutes >= min_duration_minutes:
                                available_slots.append({
                                    'date': date_obj,
                                    'start': slot_start,
                                    'end': slot_end,
                                    'start_dt': slot_start,
                                    'weekday': date_obj.weekday()  # 0=Monday, 4=Friday
                                })
                    
                    current_time = max(current_time, busy_end)
                
                # Check if there's time available after the last busy slot
                if current_time < work_end:
                    duration = work_end - current_time
                    duration_minutes = int(duration.total_seconds() // 60)
                    
                    if duration_minutes >= min_duration_minutes:
                        available_slots.append({
                            'date': date_obj,
                            'start': current_time,
                            'end': work_end,
                            'start_dt': current_time,
                            'weekday': date_obj.weekday()
                        })
                
            except ValueError:
                continue
        
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

@app.route('/check-updates')
def check_updates():
    """Check if calendar has been updated."""
    current_hash = get_calendar_hash(ICAL_URL)
    stored_hash = request.args.get('hash', '')
    
    if current_hash and current_hash != stored_hash:
        return jsonify({'changed': True, 'hash': current_hash})
    return jsonify({'changed': False, 'hash': current_hash or stored_hash})

@app.route('/')
def index():
    """Display the public calendar page with available time slots grouped by week."""
    # Get timezone from request (default to PST)
    tz_name = request.args.get('tz', 'PST')
    selected_week = request.args.get('week', None)
    
    # Get current calendar hash
    current_hash = get_calendar_hash(ICAL_URL)
    
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
        calendar_hash=current_hash or ''
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
