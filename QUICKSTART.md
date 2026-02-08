# 🚀 Quick Start Guide

Your Google Calendar sharing app is ready! Follow these simple steps:

## Step 1: Get Your Calendar's Public iCal URL

1. Open [Google Calendar](https://calendar.google.com)
2. Find your calendar in the left sidebar
3. Click the **⋮** (three dots) next to it
4. Click **"Settings and sharing"**
5. Scroll to **"Access permissions"**
6. ✅ Check **"Make available to public"**
7. Scroll to **"Integrate calendar"**
8. Copy the **"Public URL to iCal"**

## Step 2: Configure the App

Run the interactive setup:
```bash
cd google-calendar-share
source venv/bin/activate
python setup.py
```

Or manually create a `.env` file:
```bash
echo 'ICAL_URL=your-copied-url-here' > .env
```

## Step 3: Run the App

**Easy way:**
```bash
./run.sh
```

**Or manually:**
```bash
source venv/bin/activate
python app_simple.py
```

## Step 4: View Your Calendar

Open your browser:
- **Local**: http://localhost:5000
- **On your network**: http://YOUR_IP:5000

## 🎉 That's It!

Your calendar is now publicly accessible! Share the URL with anyone.

---

## Need Help?

- See `SETUP.md` for detailed instructions
- See `README.md` for full documentation
