import os
from openai import OpenAI

client = OpenAI(
    base_url="9c537b6de12144a289a07abcec45b677",
    api_key="https://api.aimlapi.com/v1",    
)

response = client.chat.completions.create(
    model="gpt-4-0613",
    messages=[
        {
            "role": "system",
            "content": "You are an AI assistant who knows everything.",
        },
        {
            "role": "user",
            "content": "Tell me, why is the sky blue?"
        },
    ],
)

message = response.choices[0].message.content

print(f"Assistant: {message}")