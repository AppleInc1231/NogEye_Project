import os
from google.cloud import texttospeech

# הצגת הנתיב לקובץ המפתח כדי לוודא שהוא מוגדר נכון
print(f"Using credentials from: {os.environ['GOOGLE_APPLICATION_CREDENTIALS']}")

# בודק אם הקובץ קיים
if not os.path.exists(os.environ['GOOGLE_APPLICATION_CREDENTIALS']):
    raise Exception(f"Error: The credentials file {os.environ['GOOGLE_APPLICATION_CREDENTIALS']} does not exist.")

# הפעלת ה-TextToSpeechClient
tts_client = texttospeech.TextToSpeechClient()

# דוגמת שימוש ב-TextToSpeech
synthesis_input = texttospeech.SynthesisInput(text="שלום, איך אפשר לעזור?")
voice = texttospeech.VoiceSelectionParams(
    language_code="he-IL", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# בקשת תוצאת דיבור
response = tts_client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# שמירת הקובץ המתקבל
with open("output.mp3", "wb") as out:
    out.write(response.audio_content)
    print("Audio content written to file 'output.mp3'")
