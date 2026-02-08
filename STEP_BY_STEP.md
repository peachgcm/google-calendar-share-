# 📋 Step-by-Step Instructions

## Step 1: Make Your Google Calendar Public

1. **Open Google Calendar**
   - Go to: https://calendar.google.com
   - Make sure you're signed in

2. **Find Your Calendar**
   - Look at the left sidebar under "My calendars"
   - Find the calendar you want to share (usually your main calendar with your name/email)

3. **Open Calendar Settings**
   - Click the **three dots (⋮)** next to your calendar name
   - Click **"Settings and sharing"**

4. **Make It Public**
   - Scroll down to the **"Access permissions"** section
   - Check the box: **"Make available to public"**
   - You'll see a warning - click "OK" to confirm

5. **Get the iCal URL**
   - Scroll further down to **"Integrate calendar"** section
   - Find **"Public URL to iCal"**
   - Click the **copy icon** or select and copy the URL
   - It will look like: `https://calendar.google.com/calendar/ical/YOUR_EMAIL/basic.ics`

## Step 2: Configure the App

You have two options:

### Option A: Use the Interactive Setup (Easiest!)
```bash
cd google-calendar-share
source venv/bin/activate
python setup.py
```
Then paste your iCal URL when prompted.

### Option B: Create .env File Manually
```bash
cd google-calendar-share
nano .env
```
Add this line (replace with your actual URL):
```
ICAL_URL=https://calendar.google.com/calendar/ical/YOUR_EMAIL/basic.ics
```
Save and exit (Ctrl+X, then Y, then Enter)

## Step 3: Run the App

```bash
cd google-calendar-share
./run.sh
```

Or manually:
```bash
source venv/bin/activate
python app_simple.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

## Step 4: View Your Calendar

Open your web browser and go to:
- **http://localhost:5000**

You should see your upcoming calendar events!

## Step 5: Share It (Optional)

To share on your local network:
1. Find your computer's IP address:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```
2. Others on your network can access: `http://YOUR_IP:5000`

To deploy publicly, see the README.md for deployment options.

---

## Troubleshooting

**"ICAL_URL not set" error?**
- Make sure you created the `.env` file
- Check that the URL starts with `https://`

**No events showing?**
- Make sure your calendar is set to "Make available to public"
- Check that you have upcoming events in your calendar
- Verify the iCal URL is correct

**Port 5000 already in use?**
- Change the port in `app_simple.py` (line 113): change `port=5000` to `port=5001`
