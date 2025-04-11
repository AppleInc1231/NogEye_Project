#!/bin/bash

# הפעלת הממשק הגרפי
cd "$(dirname "$0")/chat-ui"
npm start &

# חזרה לתיקייה הראשית והפעלת הקוד הקולי
cd ..
python3 wake_chat.py

