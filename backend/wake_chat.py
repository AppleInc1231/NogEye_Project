import openai
import os
import speech_recognition as sr
import json
from dotenv import load_dotenv
from google.cloud import texttospeech
import simpleaudio as sa
from datetime import datetime
import time

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Google TTS setup
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.path.dirname(__file__), "chat-ui", "chat-voice-key.json")
tts_client = texttospeech.TextToSpeechClient()
voice_id = "he-IL-Wavenet-C"

# קובץ זיכרון
memory_path = os.path.join(os.path.dirname(__file__), "..", "data", "memory.json")
if not os.path.exists(memory_path):
    memory = {
        "user_name": "מאור",
        "assistant_name": "צ'אט",
        "conversations": [],
        "facts": {},
        "reminders": [],
        "preferences": {
            "language": "hebrew",
            "wake_word": "צ'אט"
        }
    }
    with open(memory_path, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)
else:
    with open(memory_path, "r", encoding="utf-8") as f:
        memory = json.load(f)

def normalize_hebrew_text(text):
    corrections = {
        "היי": "שלום",
        "מה שלומך?": "מה שלומך",
        "!": "",
    }
    for wrong, right in corrections.items():
        text = text.replace(wrong, right)
    return text

def update_ui(status, user_text="", chat_text=""):
    data = {"status": status, "user": user_text, "chat": chat_text}
    
    # עדכון הנתיב לקובץ live.json שנמצא בתיקיית frontend
    live_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "live.json")
    
    try:
        with open(live_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception as e:
        print("❌ שגיאה בעדכון הממשק:", e)


def save_memory():
    with open(memory_path, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def extract_fact(user_input):
    lowered = user_input.strip()
    fact = None

    if "תזכור ש" in lowered:
        fact = lowered.split("תזכור ש")[-1].strip()
    elif "תזכור שאני" in lowered:
        fact = "אני " + lowered.split("תזכור שאני")[-1].strip()
    elif "תזכור שה" in lowered:
        fact = "ה" + lowered.split("תזכור שה")[-1].strip()
    elif lowered.startswith("תזכור"):
        print("⏳ מחכה להשלמת המשפט...")
        time.sleep(2.5)
        return "תגיד שוב את מה שאתה רוצה שאזכור."

    if fact:
        memory["facts"][str(datetime.now())] = fact
        save_memory()
        return "זכרתי את זה."

    return None

def speak(text):
    global voice_id
    try:
        text = normalize_hebrew_text(text)
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="he-IL", name=voice_id
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = tts_client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        output_path = os.path.join(os.path.dirname(__file__), "output.mp3")
        with open(output_path, "wb") as out:
            out.write(response.audio_content)

        ding_path = os.path.join(os.path.dirname(__file__), "..", "assets", "ding.wav")
        ding = sa.WaveObject.from_wave_file(ding_path)
        ding_play = ding.play()
        ding_play.wait_done()

        os.system(f"afplay '{output_path}'")

    except Exception as e:
        print("❌ שגיאה בהשמעת קול:", e)

def chat_with_gpt(prompt):
    global memory, voice_id
    update_ui("מדבר", prompt, "")
    memory["conversations"].append({"role": "user", "content": prompt})

    fact_response = extract_fact(prompt)
    if fact_response:
        answer = fact_response
    elif "צ׳אט תשנה את הקול לגבר" in prompt or "תשנה קול לגבר" in prompt:
        voice_id = "he-IL-Wavenet-D"
        answer = "עכשיו אני מדבר בקול גברי. איך אפשר לעזור?"
    elif "צ׳אט תשני את הקול לאישה" in prompt or "תשני קול לאישה" in prompt:
        voice_id = "he-IL-Wavenet-C"
        answer = "החלפתי לקול נשי. איך אפשר לעזור?"
    else:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=memory["conversations"]
        )
        answer = response.choices[0].message.content

    memory["conversations"].append({"role": "assistant", "content": answer})
    save_memory()
    update_ui("מדבר", prompt, answer)
    print("צ׳אט:", answer)
    speak(answer)

def listen_for_chat():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print("🔊 מחכה להאזנה למילת הקוד 'צ׳אט'...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    while True:
        with mic as source:
            audio = recognizer.listen(source)

        try:
            transcript = recognizer.recognize_google(audio, language="he-IL")
            if "צ׳אט" in transcript or "צ'אט" in transcript:
                cleaned = transcript.replace("צ׳אט", "").replace("צ'אט", "").strip()
                print("מקשיב: " + transcript)
                print("אתה:", cleaned)
                chat_with_gpt(cleaned)
        except Exception:
            continue

listen_for_chat()