import openai
import json

# Configuration API OpenAI
openai.api_key = "sk-mnopqrstijkl5678mnopqrstijkl5678mnopqrst"


def question_sur_ocean_et_humain(question):
    try:
        # Création de la requête à l'API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Vous êtes un assistant qui répond uniquement par 'Humain', 'Océan' ou 'Les deux', avec une explication concise."},
                {"role": "user", "content": f"Voici une question : '{question}'. Répondez en respectant les consignes."}
            ],
            temperature=0.5
        )

        # Récupération de la réponse
        answer = response['choices'][0]['message']['content'].strip()

        # Structure JSON pour la réponse
        result = {
            "question": question,
            "answer": answer
        }

        # Retourne le JSON
        return json.dumps(result, ensure_ascii=False, indent=4)

    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=4)


# Exemple d'utilisation
if __name__ == "__main__":
    question = "Qui est responsable de la montée du niveau de la mer ?"
    resultat_json = question_sur_ocean_et_humain(question)
    print(resultat_json)