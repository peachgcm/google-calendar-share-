# Google Calendar Public Sharing

A simple Flask web application to display your Google Calendar events publicly.

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Google Calendar API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google Calendar API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Calendar API"
   - Click "Enable"

4. Create OAuth 2.0 Credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Web application"
   - Add `http://localhost:5000` to authorized redirect URIs
   - Download the credentials JSON file
   - Rename it to `client_secret.json` and place it in this directory

### 3. Configure Environment Variables

Create a `.env` file in this directory:

```env
SECRET_KEY=your-secret-key-here-change-this
CALENDAR_ID=primary
```

- `SECRET_KEY`: A random secret key for Flask sessions
- `CALENDAR_ID`: Your calendar ID (use `primary` for your default calendar, or find your calendar ID in Google Calendar settings)

### 4. First-Time Authentication

Run the application:

```bash
python app.py
```

On first run, it will:
1. Open a browser window for Google authentication
2. Ask you to sign in and grant calendar access
3. Save your credentials to `token.pickle` for future use

### 5. Access Your Public Calendar

Once authenticated, visit:
- Local: `http://localhost:5000`
- Network: `http://YOUR_IP:5000` (to share on your local network)

## Two Options Available

### Option 1: Simple iCal Feed (Recommended - Easier!)

Use `app_simple.py` which reads from your calendar's public iCal feed. No authentication needed!

1. Make your Google Calendar public:
   - Go to Google Calendar
   - Click the three dots (⋮) next to your calendar
   - Select "Settings and sharing"
   - Under "Access permissions", check "Make available to public"
   - Scroll to "Integrate calendar" section
   - Copy the "Public URL to iCal"

2. Set the URL in `.env`:
   ```env
   ICAL_URL=https://calendar.google.com/calendar/ical/your-calendar-id/public/basic.ics
   ```

3. Run the simple version:
   ```bash
   python app_simple.py
   ```

### Option 2: Full OAuth API (More Features)

Use `app.py` for full Google Calendar API access with OAuth authentication.

## Deployment Options

You can deploy this to services like:
- **Heroku**: Add a `Procfile` with `web: python app_simple.py`
- **Railway**: Connect your GitHub repo
- **Render**: Deploy from GitHub
- **PythonAnywhere**: Upload files and configure
- **Fly.io**: Deploy with Docker

## Security Notes

- The `token.pickle` file contains your credentials - don't commit it to version control
- Add `token.pickle` and `client_secret.json` to `.gitignore`
- For production, use environment variables for sensitive data
- Consider using a service account for better security in production

## Troubleshooting

- **"client_secret.json not found"**: Make sure you've downloaded and renamed the OAuth credentials file
- **Authentication errors**: Delete `token.pickle` and re-authenticate
- **No events showing**: Check that your `CALENDAR_ID` is correct and the calendar has events
