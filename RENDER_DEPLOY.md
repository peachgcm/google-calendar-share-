# 🚀 Deploy to Render - Step by Step Guide

Follow these steps to deploy your calendar app to Render.com

## Prerequisites
- GitHub account (free)
- Your Google Calendar iCal URL: `https://calendar.google.com/calendar/ical/pjiang%40surveymonkey.com/public/basic.ics`

---

## Step 1: Initialize Git Repository

Run these commands in your terminal:

```bash
cd "/Users/pjiang/Documents/New Folder With Items/miniProjects/google-calendar-share"

# Initialize git
git init

# Add all files (except those in .gitignore)
git add .

# Make initial commit
git commit -m "Initial commit - Calendar app ready for Render"
```

---

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `google-calendar-share` (or any name you like)
3. Description: "Public Google Calendar sharing app"
4. Choose **Public** (or Private if you prefer)
5. **DO NOT** initialize with README, .gitignore, or license
6. Click **"Create repository"**

---

## Step 3: Push to GitHub

After creating the repo, GitHub will show you commands. Run these:

```bash
# Add your GitHub repo as remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/google-calendar-share.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Step 4: Deploy on Render

### 4.1 Sign Up / Login
1. Go to https://render.com
2. Click **"Get Started for Free"**
3. Sign up with **GitHub** (recommended - one click)
4. Authorize Render to access your GitHub

### 4.2 Create New Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. You'll see a list of your GitHub repositories
4. Click **"Connect"** next to your `google-calendar-share` repository

### 4.3 Configure Your Service

Fill in these settings:

**Basic Settings:**
- **Name:** `google-calendar-share` (or any name)
- **Region:** Choose closest to you (e.g., `Oregon (US West)`)
- **Branch:** `main` (should be auto-selected)
- **Root Directory:** Leave empty (or `./` if needed)
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python app_simple.py`

**Advanced Settings (click to expand):**
- **Auto-Deploy:** `Yes` (deploys automatically on git push)
- **Health Check Path:** `/` (optional)

### 4.4 Add Environment Variable

**IMPORTANT:** You need to add your iCal URL as an environment variable.

1. Scroll down to **"Environment Variables"** section
2. Click **"Add Environment Variable"**
3. Add:
   - **Key:** `ICAL_URL`
   - **Value:** `https://calendar.google.com/calendar/ical/pjiang%40surveymonkey.com/public/basic.ics`
4. Click **"Add"**

### 4.5 Deploy!

1. Scroll to bottom
2. Click **"Create Web Service"**
3. Wait 5-10 minutes for deployment
4. You'll see build logs in real-time

---

## Step 5: Your App is Live! 🎉

Once deployment completes:
- Your app will be live at: `https://google-calendar-share.onrender.com` (or your chosen name)
- Share this URL with anyone!
- The app will automatically refresh every 2 minutes

---

## Troubleshooting

### Build Fails?
- Check that `requirements.txt` is correct
- Make sure Python version is compatible (3.9+)
- Check build logs for specific errors

### App Doesn't Load?
- Verify `ICAL_URL` environment variable is set correctly
- Check that your Google Calendar is set to "Make available to public"
- Look at service logs in Render dashboard

### Port Issues?
- The app automatically uses the `PORT` environment variable
- Render sets this automatically - no action needed

### Need to Update?
- Just push to GitHub: `git push`
- Render will auto-deploy (if Auto-Deploy is enabled)

---

## Free Tier Notes

Render's free tier:
- ✅ Free forever
- ⚠️ Spins down after 15 minutes of inactivity
- ⚠️ First request after spin-down takes ~30 seconds
- 💰 Upgrade to paid ($7/month) for always-on service

---

## Next Steps

1. ✅ Test your deployed app
2. ✅ Share the URL with others
3. ✅ Bookmark your Render dashboard
4. ✅ Set up custom domain (optional, paid feature)

---

## Quick Commands Reference

```bash
# Update your app
git add .
git commit -m "Update calendar app"
git push

# View logs (in Render dashboard)
# Go to your service → Logs tab
```

---

**Need help?** Check Render's docs: https://render.com/docs
