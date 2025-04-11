import openai

openai.api_key = "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"

response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "אתה עוזר אישי בשם צ׳אט"},
        {"role": "user", "content": "שלום, איך אתה מרגיש היום?"}
    ]
)

print("צ׳אט:", response.choices[0].message.content)


