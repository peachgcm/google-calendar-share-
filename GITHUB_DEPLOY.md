# 🚀 GitHub Deployment Guide - Step by Step

Follow these steps to deploy your calendar app to Render using GitHub.

## Prerequisites
- ✅ Your code is ready (all files committed)
- ✅ Your Google Calendar iCal URL: `https://calendar.google.com/calendar/ical/pjiang%40surveymonkey.com/public/basic.ics`
- ✅ GitHub account (free)

---

## Step 1: Push Your Code to GitHub

### 1.1 Check Current Status
```bash
cd "/Users/pjiang/Documents/New Folder With Items/miniProjects/google-calendar-share"
git status
```

### 1.2 Commit Any Uncommitted Changes
If you have uncommitted changes:
```bash
git add .
git commit -m "Update calendar app with smart refresh"
```

### 1.3 Create GitHub Repository

**Option A: Using GitHub Website (Recommended)**
1. Go to https://github.com/new
2. Repository name: `google-calendar-share` (or any name you like)
3. Description: "Public Google Calendar sharing app"
4. Choose **Public** (or Private if you prefer)
5. **DO NOT** check "Initialize with README" or any other options
6. Click **"Create repository"**

**Option B: Using GitHub CLI (if installed)**
```bash
gh repo create google-calendar-share --public --source=. --remote=origin --push
```

### 1.4 Push to GitHub

After creating the repo, GitHub will show you commands. Run these:

```bash
# Add GitHub as remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/google-calendar-share.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**If you already have a remote:**
```bash
# Check existing remote
git remote -v

# If needed, update remote URL
git remote set-url origin https://github.com/YOUR_USERNAME/google-calendar-share.git

# Push
git push -u origin main
```

---

## Step 2: Deploy to Render

### 2.1 Sign Up / Login
1. Go to https://render.com
2. Click **"Get Started for Free"**
3. Sign up with **GitHub** (one-click signup)
4. Authorize Render to access your GitHub repositories

### 2.2 Create New Web Service
1. In Render dashboard, click **"New +"** button (top right)
2. Select **"Web Service"**
3. You'll see a list of your GitHub repositories
4. Find and click **"Connect"** next to your `google-calendar-share` repository

### 2.3 Configure Your Service

Fill in these settings:

**Basic Settings:**
- **Name:** `google-calendar-share` (or any name)
- **Region:** Choose closest to you (e.g., `Oregon (US West)`)
- **Branch:** `main` (should be auto-selected)
- **Root Directory:** Leave empty
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python app_simple.py`

**Advanced Settings (optional):**
- **Auto-Deploy:** `Yes` (deploys automatically when you push to GitHub)
- **Health Check Path:** `/` (optional)

### 2.4 Add Environment Variable

**CRITICAL:** You must add your iCal URL as an environment variable.

1. Scroll down to **"Environment Variables"** section
2. Click **"Add Environment Variable"**
3. Add:
   - **Key:** `ICAL_URL`
   - **Value:** `https://calendar.google.com/calendar/ical/pjiang%40surveymonkey.com/public/basic.ics`
4. Click **"Add"**

**Important:** Never commit your `.env` file to GitHub! It's already in `.gitignore`.

### 2.5 Deploy!

1. Scroll to bottom of the page
2. Click **"Create Web Service"**
3. Wait 5-10 minutes for deployment
4. Watch the build logs in real-time

---

## Step 3: Your App is Live! 🎉

Once deployment completes:
- ✅ Your app will be live at: `https://google-calendar-share.onrender.com` (or your chosen name)
- ✅ Share this URL with anyone!
- ✅ The app will automatically update when you push changes to GitHub

---

## Step 4: Updating Your App

After making changes locally:

```bash
# 1. Make your changes to files
# 2. Commit changes
git add .
git commit -m "Description of changes"

# 3. Push to GitHub
git push

# 4. Render will automatically deploy (if Auto-Deploy is enabled)
```

---

## Troubleshooting

### Build Fails?
- ✅ Check that `requirements.txt` has all dependencies
- ✅ Verify Python version compatibility
- ✅ Check build logs in Render dashboard for specific errors

### App Doesn't Load?
- ✅ Verify `ICAL_URL` environment variable is set correctly in Render
- ✅ Check that your Google Calendar is set to "Make available to public"
- ✅ Look at service logs in Render dashboard

### Environment Variable Not Working?
- ✅ Make sure it's named exactly `ICAL_URL` (case-sensitive)
- ✅ Verify the value is correct (your iCal URL)
- ✅ Redeploy after adding/changing environment variables

### Port Issues?
- ✅ The app automatically uses the `PORT` environment variable
- ✅ Render sets this automatically - no action needed

---

## Quick Reference

**Your iCal URL:**
```
ICAL_URL=https://calendar.google.com/calendar/ical/pjiang%40surveymonkey.com/public/basic.ics
```

**GitHub Repository:**
```
https://github.com/YOUR_USERNAME/google-calendar-share
```

**Render Service:**
```
https://google-calendar-share.onrender.com
```

---

## Security Notes

✅ **DO:**
- Keep `.env` file local (it's in `.gitignore`)
- Use environment variables in Render for sensitive data
- Make repository private if you prefer

❌ **DON'T:**
- Commit `.env` file to GitHub
- Share your iCal URL publicly (though it's already public)
- Commit credentials or tokens

---

## Next Steps After Deployment

1. ✅ Test your deployed app
2. ✅ Share the URL with others
3. ✅ Bookmark your Render dashboard
4. ✅ Set up custom domain (optional, paid feature)

---

**Need help?** Check Render's docs: https://render.com/docs
