import openai
from django.conf import settings

def bot_response(user_message):
    openai.api_key = settings.OPENAI_API_KEY

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # lightweight & cheap, or "gpt-4o" for full
        messages=[
            {"role": "system", "content": "You are a helpful support assistant for a car dealership website."},
            {"role": "user", "content": user_message},
        ]
    )

    return response["choices"][0]["message"]["content"]
