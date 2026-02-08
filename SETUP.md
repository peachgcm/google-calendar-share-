# Quick Setup Guide

## Step 1: Get Your Google Calendar Public iCal URL

1. Go to [Google Calendar](https://calendar.google.com)
2. On the left sidebar, find your calendar under "My calendars"
3. Click the **three dots (⋮)** next to your calendar name
4. Select **"Settings and sharing"**
5. Scroll down to **"Access permissions"** section
6. Check the box: **"Make available to public"**
7. Scroll further down to **"Integrate calendar"** section
8. Copy the **"Public URL to iCal"** - it looks like:
   ```
   https://calendar.google.com/calendar/ical/YOUR_EMAIL/basic.ics
   ```

## Step 2: Configure the App

Create a `.env` file in this directory with your iCal URL:

```bash
echo 'ICAL_URL=https://calendar.google.com/calendar/ical/YOUR_EMAIL/basic.ics' > .env
```

Or manually create `.env` and add:
```
ICAL_URL=your-copied-url-here
```

## Step 3: Run the App

**Option A: Use the run script**
```bash
chmod +x run.sh
./run.sh
```

**Option B: Manual run**
```bash
source venv/bin/activate
python app_simple.py
```

## Step 4: Access Your Calendar

Open your browser and go to:
- **Local**: http://localhost:5000
- **On your network**: http://YOUR_IP_ADDRESS:5000

To find your IP address:
- Mac/Linux: `ifconfig | grep "inet "`
- Or check System Settings > Network

## Troubleshooting

**No events showing?**
- Make sure your calendar is set to "Make available to public"
- Verify the iCal URL is correct in your `.env` file
- Check that your calendar has upcoming events

**Port already in use?**
- Change the port in `app_simple.py`: `app.run(host='0.0.0.0', port=5001, debug=True)`
