from backend.database.db_setup import db
from mistralai import Mistral

class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Enum('L\'Humain', 'L\'Océan', 'Les deux', name='answer_enum'), nullable=False)

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def get_question(self):
        return self.question

    def get_answer(self):
        return self.answer

    def set_question(self, question):
        self.question = question
        db.session.commit()

    def set_answer(self, answer):
        if answer not in ['Humain', 'Océon', 'Les deux']:
            raise ValueError("Answer must be one of: 'Humain', 'Océon', 'Les deux'")
        self.answer = answer
        db.session.commit()

    def delete_question(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_questions():
        return [{'id':quiz.id, 'question':quiz.question, 'answer':quiz.answer} for quiz in Quiz.query.all()]

    @staticmethod
    def add_question(question, answer):
        if answer not in ['Humain', 'Océon', 'Les deux']:
            raise ValueError("Answer must be one of: 'Humain', 'Océon', 'Les deux'")
        new_quiz = Quiz(question=question, answer=answer)
        db.session.add(new_quiz)
        db.session.commit()


    @staticmethod
    def get_question_by_id(question_id):
        quiz = Quiz.query.get(question_id)
        if quiz:
            return {
                "id": quiz.id,
                "question": quiz.question,
                "answer": quiz.answer
            }
        else:
            return None

    @staticmethod
    def get_ia_quiz(nbr=10):
        api_key = "DNsdA0tKnjs4UdEwouT67KdCFWzO77ro"
        model = "mistral-large-latest"

        client = Mistral(api_key=api_key)

        chat_response = client.chat.complete(
            model= model,
            messages = [
                {
                    "role": "user",
                    "content": f'Génère une liste de {nbr} questions avec 3 réponses possibles (L\'Océan, L\'Humain, Les deux) et donne la réponse correcte.Format attendu :[{"question": "Votre question ici",answer": "Réponse correcte"}, ...]',
                },
            ]
        )
        return chat_response.choices[0].message.content