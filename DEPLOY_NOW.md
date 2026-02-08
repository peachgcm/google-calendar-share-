# 🚀 Ready to Deploy to Render!

Your code is ready! Follow these steps:

## ✅ What's Done
- ✅ Git repository initialized
- ✅ All files committed
- ✅ .env file is safely ignored (won't be uploaded)
- ✅ Deployment files created

## 📋 Next Steps

### 1. Create GitHub Repository
Go to: https://github.com/new
- Name: `google-calendar-share`
- Make it Public
- **Don't** initialize with README
- Click "Create repository"

### 2. Push to GitHub
Run these commands (replace YOUR_USERNAME):

```bash
cd "/Users/pjiang/Documents/New Folder With Items/miniProjects/google-calendar-share"
git remote add origin https://github.com/YOUR_USERNAME/google-calendar-share.git
git branch -M main
git push -u origin main
```

### 3. Deploy on Render
1. Go to: https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your `google-calendar-share` repo
5. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app_simple.py`
6. **Add Environment Variable:**
   - Key: `ICAL_URL`
   - Value: `https://calendar.google.com/calendar/ical/pjiang%40surveymonkey.com/public/basic.ics`
7. Click "Create Web Service"
8. Wait 5-10 minutes
9. **Done!** 🎉

## 📖 Detailed Guide
See `RENDER_DEPLOY.md` for complete step-by-step instructions with screenshots guidance.

## 🔗 Your App Will Be Live At:
`https://google-calendar-share.onrender.com` (or your chosen name)

---

**Quick Tip:** After deployment, test your app and share the URL with others!
