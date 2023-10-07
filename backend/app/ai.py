import os
import openai

from app.settings import OPEN_AI_ENDPOINT, OPEN_AI_API_KEY, OPEN_AI_ENGINE

openai.api_type = "azure"
openai.api_base = OPEN_AI_ENDPOINT
openai.api_version = "2023-07-01-preview"
openai.api_key = OPEN_AI_API_KEY


def analyze(message):
    response = openai.ChatCompletion.create(
        engine=OPEN_AI_ENGINE,
        messages=[
            {
                "role": "system",
                "content": "You are an water resources expert, you want to give some suggestion to the public.",
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    )

    return response['choices'][0].to_dict()['message']['content']
