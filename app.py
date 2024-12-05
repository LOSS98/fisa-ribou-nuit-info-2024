from flask import Flask, jsonify
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

@app.route('/api/quiz/<int:question_id>', methods=['GET'])
def get_question(question_id):
    ''''Get a question by its ID
    Return : {id, question, answer} or {error}'''
    question = Quiz.get_question_by_id(question_id)
    if question:
        return jsonify(question), 200
    else:
        return jsonify({"error": "Question not found"}), 404

# Exemple de point de départ
if __name__ == '__main__':
    app.run(debug=True)