const fs = require('fs');
const path = require('path');

// חיבור לאלמנטים במסך
const userTextEl = document.getElementById("user-text");
const chatTextEl = document.getElementById("chat-text");
const statusEl = document.getElementById("status");
const tempEl = document.getElementById("temperature");
const waveEls = document.querySelectorAll(".wave");

// עדכון נתיב הקובץ live.json לפי הנתיב החדש
function updateFromJSON() {
  const filePath = path.join(__dirname, '..', 'frontend', 'live.json'); // עדכון נתיב הקובץ

  fs.readFile(filePath, "utf8", (err, data) => {
    if (err) {
      console.error("❌ שגיאה בקריאת הקובץ:", err);
      return;
    }

    try {
      const parsed = JSON.parse(data);

      // מעדכן טקסטים במסך
      statusEl.textContent = parsed.status || "מוכן";
      userTextEl.textContent = parsed.user || "";
      chatTextEl.textContent = parsed.chat || "";

      // מפעיל/מכבה את הגלים לפי מצב
      if (parsed.status === "מאזין") {
        waveEls.forEach(wave => wave.style.opacity = "1");
      } else {
        waveEls.forEach(wave => wave.style.opacity = "0.2");
      }

    } catch (e) {
      console.error("❌ שגיאה בפענוח JSON:", e);
    }
  });
}

// טוען מזג אוויר מדאלאס
async function loadWeather() {
  try {
    const res = await fetch("https://api.open-meteo.com/v1/forecast?latitude=32.7767&longitude=-96.7970&current_weather=true");
    const data = await res.json();
    tempEl.textContent = data.current_weather.temperature;
  } catch {
    tempEl.textContent = "שגיאה";
  }
}

loadWeather();
setInterval(updateFromJSON, 500); // עדכון כל חצי שנייה
