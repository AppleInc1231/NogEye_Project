import openai
import os

# המפתח שלך משולב כאן:
openai.api_key = "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"

# פונקציית דיבור
def speak(text):
    os.system(f'say "{text}"')

# שיחה עם GPT
def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "אתה עוזר אישי בשם צ׳אט. דבר בעברית."},
            {"role": "user", "content": prompt}
        ]
    )
    answer = response.choices[0].message.content
    print("צ׳אט:", answer)
    speak(answer)

# הרצה בלולאה
while True:
    user_input = input("אתה: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    chat_with_gpt(user_input)
