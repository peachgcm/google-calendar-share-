from flask import Flask, render_template
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

# Google Calendar API configuration
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CLIENT_SECRETS_FILE = 'client_secret.json'
CALENDAR_ID = os.environ.get('CALENDAR_ID', 'primary')  # Use 'primary' for default calendar

def get_calendar_service():
    """Get authenticated Google Calendar service."""
    creds = None
    
    # Check if we have stored credentials
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, user needs to authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # For public sharing, you might want to use a service account
            # or pre-authenticate and store credentials
            if not os.path.exists(CLIENT_SECRETS_FILE):
                raise Exception(
                    f"Please create {CLIENT_SECRETS_FILE} with your Google OAuth credentials. "
                    "See README.md for instructions."
                )
            
            flow = Flow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('calendar', 'v3', credentials=creds)

def get_upcoming_events(max_results=10):
    """Fetch upcoming events from Google Calendar."""
    try:
        service = get_calendar_service()
        
        # Get current time and time 30 days from now
        now = datetime.utcnow().isoformat() + 'Z'
        time_max = (datetime.utcnow() + timedelta(days=30)).isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=now,
            timeMax=time_max,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        # Format events for display
        formatted_events = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            # Parse datetime
            if 'T' in start:
                start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
                start_str = start_dt.strftime('%B %d, %Y at %I:%M %p')
                end_str = end_dt.strftime('%I:%M %p')
                time_str = f"{start_str} - {end_str}"
            else:
                start_dt = datetime.fromisoformat(start)
                time_str = start_dt.strftime('%B %d, %Y (All Day)')
            
            formatted_events.append({
                'summary': event.get('summary', 'No Title'),
                'time': time_str,
                'description': event.get('description', ''),
                'location': event.get('location', ''),
                'htmlLink': event.get('htmlLink', '')
            })
        
        return formatted_events
    except Exception as e:
        print(f"Error fetching events: {e}")
        return []

@app.route('/')
def index():
    """Display the public calendar page."""
    events = get_upcoming_events(max_results=20)
    return render_template('calendar.html', events=events)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
