# 🚀 Quick Deployment Guide

Deploy your calendar app to the cloud in minutes!

## ⚡ Fastest Option: Render (Recommended)

### Step 1: Prepare Your Code
```bash
cd google-calendar-share
# Make sure .env is NOT committed (it's in .gitignore)
git init
git add .
git commit -m "Initial commit"
```

### Step 2: Push to GitHub
1. Create a new repository on GitHub
2. Push your code:
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### Step 3: Deploy on Render
1. Go to https://render.com
2. Sign up/login (free with GitHub)
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository
5. Configure:
   - **Name:** `my-calendar-app` (or any name)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app_simple.py`
   - **Add Environment Variable:**
     - Key: `ICAL_URL`
     - Value: Your Google Calendar iCal URL
6. Click **"Create Web Service"**
7. Wait 5-10 minutes for deployment
8. **Done!** Your app is live at: `https://your-app-name.onrender.com`

---

## 🚂 Alternative: Railway (Also Easy)

1. Go to https://railway.app
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repository
5. Add environment variable: `ICAL_URL` = your iCal URL
6. Railway auto-detects and deploys!
7. **Done!** Your app is live

---

## 🐳 Docker Deployment (Any Platform)

If you want to use Docker:

1. Build the image:
```bash
docker build -t calendar-app .
```

2. Run locally:
```bash
docker run -p 5001:5001 -e ICAL_URL="your-url" calendar-app
```

3. Push to Docker Hub and deploy to any service that supports Docker

---

## 📝 Important Notes

✅ **Your `.env` file is already in `.gitignore`** - it won't be committed  
✅ **Set `ICAL_URL` as an environment variable** in your hosting service  
✅ **The app automatically uses the `PORT` environment variable** (cloud services set this)  
✅ **Debug mode is disabled in production** for security  

---

## 🔗 Share Your Calendar

Once deployed, share your public URL with anyone! They can:
- View your available time slots
- See times in all 4 US time zones (PST, MST, CST, EST)
- Select different weeks
- See times automatically update

---

## ❓ Need Help?

If you run into issues:
1. Check that `ICAL_URL` is set correctly
2. Make sure your Google Calendar is set to "Make available to public"
3. Check the deployment logs in your hosting service
