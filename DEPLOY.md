# Deploying Your Calendar App to Public Services

This guide will help you deploy your Google Calendar sharing app to various public hosting services.

## Prerequisites

1. Make sure your `.env` file has your `ICAL_URL` set
2. Your Google Calendar must be set to "Make available to public"
3. Have a GitHub account (for most services)

---

## Option 1: Render (Recommended - Free Tier Available)

**Steps:**

1. **Create a GitHub repository:**
   ```bash
   cd google-calendar-share
   git init
   git add .
   git commit -m "Initial commit"
   # Create a repo on GitHub and push
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Go to Render:**
   - Visit https://render.com
   - Sign up/login with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure:**
   - **Name:** `your-calendar-app` (or any name)
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app_simple.py`
   - **Environment Variables:**
     - `ICAL_URL`: Your Google Calendar iCal URL
   - **Port:** Leave default (Render auto-detects)

4. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Your app will be live at: `https://your-calendar-app.onrender.com`

**Note:** Free tier may spin down after inactivity. Upgrade to paid for always-on.

---

## Option 2: Railway (Easy Deployment)

**Steps:**

1. **Install Railway CLI (optional):**
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy:**
   - Go to https://railway.app
   - Sign up/login with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Add environment variable:
     - `ICAL_URL`: Your Google Calendar iCal URL
   - Railway auto-detects Python and deploys

3. **Your app will be live at:** `https://your-app-name.up.railway.app`

**Note:** Railway offers $5/month credit for free tier.

---

## Option 3: Fly.io (Global Edge Deployment)

**Steps:**

1. **Install Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Create fly.toml:**
   ```bash
   fly launch
   ```
   (This will create the config file)

3. **Set environment variable:**
   ```bash
   fly secrets set ICAL_URL="your-ical-url-here"
   ```

4. **Deploy:**
   ```bash
   fly deploy
   ```

**Your app will be live at:** `https://your-app-name.fly.dev`

---

## Option 4: PythonAnywhere (Simple & Free)

**Steps:**

1. **Sign up:** https://www.pythonanywhere.com (free account)

2. **Upload files:**
   - Go to "Files" tab
   - Upload all files from `google-calendar-share/`
   - Create `.env` file with your `ICAL_URL`

3. **Set up virtual environment:**
   - Go to "Consoles" → "Bash"
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Create Web App:**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Flask" → Python 3.10
   - Set source code: `/home/yourusername/google-calendar-share`
   - Edit WSGI file to point to `app_simple.py`

5. **Reload:** Click "Reload" button

**Your app will be live at:** `https://yourusername.pythonanywhere.com`

---

## Option 5: Replit (Quick & Easy)

**Steps:**

1. **Go to Replit:** https://replit.com
2. **Create new Repl:** "Import from GitHub"
3. **Select your repository**
4. **Set environment variable:**
   - Click "Secrets" (lock icon)
   - Add `ICAL_URL` with your value
5. **Run:** Click "Run" button
6. **Share:** Click "Share" → "Copy link"

**Your app will be live at:** `https://your-repl-name.your-username.repl.co`

---

## Important Notes for All Services

### Environment Variables
Make sure to set `ICAL_URL` in your hosting service's environment variables section. **Never commit your `.env` file to GitHub!**

### Port Configuration
Some services require specific port handling. Update `app_simple.py` if needed:
```python
import os
port = int(os.environ.get('PORT', 5001))
app.run(host='0.0.0.0', port=port, debug=False)
```

### Security
- Remove `debug=True` for production
- Use environment variables for sensitive data
- Don't commit `.env` or `token.pickle` files

---

## Quick Deploy Script

I can help you set up deployment for any of these services. Which one would you like to use?
