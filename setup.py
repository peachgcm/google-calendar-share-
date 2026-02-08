#!/usr/bin/env python3
"""
Interactive setup script for Google Calendar sharing app.
"""
import os
from pathlib import Path

def main():
    print("=" * 60)
    print("Google Calendar Public Sharing - Setup")
    print("=" * 60)
    print()
    
    env_file = Path(".env")
    
    # Check if .env already exists
    if env_file.exists():
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/n): ").strip().lower()
        if response != 'y':
            print("Setup cancelled.")
            return
    
    print("To get your Google Calendar public iCal URL:")
    print()
    print("1. Go to https://calendar.google.com")
    print("2. Click the three dots (⋮) next to your calendar")
    print("3. Select 'Settings and sharing'")
    print("4. Under 'Access permissions', check 'Make available to public'")
    print("5. Scroll to 'Integrate calendar' section")
    print("6. Copy the 'Public URL to iCal'")
    print()
    
    ical_url = input("Paste your iCal URL here: ").strip()
    
    if not ical_url:
        print("❌ No URL provided. Setup cancelled.")
        return
    
    if not ical_url.startswith('http'):
        print("⚠️  Warning: URL doesn't start with http/https. Make sure it's correct!")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            return
    
    # Write .env file
    env_content = f"ICAL_URL={ical_url}\n"
    env_file.write_text(env_content)
    
    print()
    print("✅ .env file created successfully!")
    print()
    print("Next steps:")
    print("1. Run the app: ./run.sh")
    print("   Or: source venv/bin/activate && python app_simple.py")
    print("2. Open http://localhost:5000 in your browser")
    print()

if __name__ == "__main__":
    main()
