from flask import Flask, jsonify, request
from flask_assets import Environment, Bundle
from database.db_setup import db
from entities.quiz import Quiz

app = Flask(__name__)
assets = Environment(app)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'idfghjkagfuykagsf76GHKSGDFJ87vk'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nuit_info.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

'''Quiz API'''
@app.route('/api/quiz/<int:question_id>', methods=['GET'])
def get_question(question_id):
    ''''Get a question by its ID
    Return : {id, question, answer} or {error}'''
    question = Quiz.get_question_by_id(question_id)
    if question:
        return jsonify(question), 200
    else:
        return jsonify({"error": "Question not found"}), 404

@app.route('/api/quiz', methods=['GET'])
def get_all_questions():
    '''Get all questions
    Return : [question1, question2, ...]'''
    questions = Quiz.get_all_questions()
    return jsonify(questions), 200

@app.route('/api/quiz', methods=['POST'])
def add_question():
    '''Add a question
    Request : {"question": "Question", "answer": "Humain|Océon|Les deux"}
    Return : {id, question, answer} or {error}'''
    data = request.get_json()
    try:
        Quiz.add_question(data['question'], data['answer'])
        return jsonify({"message": "Question added"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/quiz', methods=['PUT'])
def update_question():
    '''Update a question
    Request : {"id": 1, "question": "Question", "answer": "Humain|Océon|Les deux"}
    Return : {id, question, answer} or {error}'''
    data = request.get_json()
    try:
        question = Quiz.get_question_by_id(data['id'])
        if question:
            question.set_question(data['question'])
            question.set_answer(data['answer'])
            return jsonify(question), 200
        else:
            return jsonify({"error": "Question not found"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/quiz/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    '''Delete a question
    Return : {message} or {error}'''
    question = Quiz.get_question_by_id(question_id)
    if question:
        question.delete_question()
        return jsonify({"message": "Question deleted"}), 200
    else:
        return jsonify({"error": "Question not found"}), 404


'''END Quiz API'''

if __name__ == '__main__':
    app.run(debug=True)