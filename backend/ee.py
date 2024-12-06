import os
from mistralai import Mistral
api_key = "DNsdA0tKnjs4UdEwouT67KdCFWzO77ro"
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

chat_response = client.chat.complete(
    model= model,
    messages = [
        {
            "role": "user",
            "content": 'Génère une liste de 10 questions avec 3 réponses possibles (L\'Océan, L\'Humain, Les deux) et donne la réponse correcte.Format attendu :[{"question": "Votre question ici",answer": "Réponse correcte"}, ...]',
        },
    ]
)
print(chat_response.choices[0].message.content)