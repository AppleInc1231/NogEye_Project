from google.cloud import texttospeech
import os

# קובץ המפתח
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "chat-voice-key.json"

# יצירת לקוח
tts_client = texttospeech.TextToSpeechClient()

# טקסט לדיבור
synthesis_input = texttospeech.SynthesisInput(text="שלום, מה שלומך היום?")

# קול עברי גברי
voice = texttospeech.VoiceSelectionParams(
    language_code="he-IL",
    name="he-IL-Wavenet-D"
)

# הגדרות אודיו
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# יצירת הקובץ
response = tts_client.synthesize_speech(
    input=synthesis_input,
    voice=voice,
    audio_config=audio_config
)

# שמירה וניגון
with open("test.mp3", "wb") as out:
    out.write(response.audio_content)

os.system("afplay test.mp3")

