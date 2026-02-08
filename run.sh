#!/bin/bash
# Simple script to run the calendar app

cd "$(dirname "$0")"
source venv/bin/activate
python app_simple.py
