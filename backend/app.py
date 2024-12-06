from flask import Flask, jsonify, request
from flask_assets import Environment, Bundle
from flask_cors import CORS

from backend.entities.admin import Admin
from backend.database.db_setup import db
from backend.entities.podcast import Podcast
from backend.entities.quiz import Quiz
from backend.entities.streak import Streak
from backend.entities.video import Video

app = Flask(__name__)
assets = Environment(app)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'idfghjkagfuykagsf76GHKSGDFJ87vk'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nuit_info.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
app.config['CORS_HEADERS'] = 'Content-Type'

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

'''Admin API'''
@app.route('/api/admin/<int:admin_id>', methods=['GET'])
def get_admin_by_id(admin_id):
    """
    Récupère un administrateur par son ID.
    Request : admin_id (int)
    Return : {"id": <ID>, "email": <EMAIL>} ou {"error": "Admin not found"}
    """
    admin = Admin.get_admin_by_id(admin_id)  # Appel de la méthode du modèle
    if admin:
        return jsonify(admin), 200
    else:
        return jsonify({"error": f"Admin with ID {admin_id} not found"}), 404

@app.route('/api/admin/<string:admin_email>', methods=['GET'])
def get_admin_by_email(admin_email):
    """
    Récupère un administrateur par son email.
    Retour : {"id": <ID>, "email": <EMAIL>} ou {"error": "Admin not found"}
    """
    admin = Admin.get_admin_by_email(admin_email)  # Appel de la méthode statique
    if admin:
        return jsonify(admin), 200
    else:
        return jsonify({"error": "Admin not found"}), 404

@app.route('/api/admin/<int:admin_id>', methods=['PUT'])
def update_admin_by_id(admin_id):
    '''Update a admin by its ID
    Return : {id, question, answer} or {error}'''
    data = request.get_json()
    try:
        admin = Admin.get_admin_by_id(admin_id)
        if admin:
            admin.set_email(data['email'])
            admin.set_password(data['password'])
            return jsonify(admin), 200
        else:
            return jsonify({"error": "Admin not found"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/admin/<string:admin_email>', methods=['PUT'])
def update_admin_by_email(admin_email):
    '''Update a admin by its Email
    Return : {id, question, answer} or {error}'''
    data = request.get_json()
    try:
        admin = Admin.get_admin_by_email(admin_email)
        if admin:
            admin.set_email(data['email'])
            admin.set_password(data['password'])
            return jsonify(admin), 200
        else:
            return jsonify({"error": "Admin not found"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/admin/<int:admin_id>', methods=['POST'])
def add_admin():
    '''Add a admin
    Request : {"email": "<EMAIL>", "password": "<PASSWORD>"}'''
    data = request.get_json()
    try:
        Admin.add_admin(data['email'], data['password'])
        return jsonify({"message": "Admin added"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/admin/<string:admin_email>', methods=['DELETE'])
def delete_admin_by_email(admin_email):
    '''Delete a admin
    Return : {message} or {error}'''
    admin = Admin.get_admin_by_email(admin_email)
    if admin:
        admin.delete_admin()
        return jsonify({"message": "Admin deleted"}), 200
    else:
        return jsonify({"error": "Admin not found"}), 404

@app.route('/api/admin/<int:admin_id>', methods=['DELETE'])
def delete_admin_by_id(admin_id):
    '''Delete a admin
    Return : {message} or {error}'''
    admin = Admin.get_admin_by_id(admin_id)
    if admin:
        admin.delete_admin()
        return jsonify({"message": "Admin deleted"}), 200
    else:
        return jsonify({"error": "Admin not found"}), 404
'''END Admin API'''

'''Streak API'''

@app.route('/api/streak/<int:streak_id>', methods=['GET'])
def get_streak_by_id(streak_id):
    '''Get a streak by its ID
    Return : {id, pseudo, streak, date} or {error}'''
    streak = Streak.get_streak_by_id(streak_id)
    if streak:
        return jsonify(streak), 200
    else:
        return jsonify({"error": "Streak not found"}), 404

@app.route('/api/streak', methods=['GET'])
def get_all_streaks():
    '''Get all streaks
    Return : [streak1, streak2, ...]'''
    streaks = Streak.get_all_streaks()
    return jsonify(streaks), 200

@app.route('/api/streak', methods=['POST'])
def add_streak():
    '''Add a streak
    Request : {"pseudo": "<PSEUDO>", "streak": <STREAK>, "date": "<DATE>"}
    Return : {id, pseudo, streak, date} or {error}'''
    data = request.get_json()
    try:
        Streak.add_streak(data['pseudo'], data['streak'], data['date'])
        return jsonify({"message": "Streak added"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/streak', methods=['PUT'])
def update_streak():
    '''Update a streak
    Request : {"id": 1, "pseudo": "<PSEUDO>", "streak": <STREAK>, "date": "<DATE>"}
    Return : {id, pseudo, streak, date} or {error}'''
    data = request.get_json()
    try:
        streak = Streak.get_streak_by_id(data['id'])
        if streak:
            streak.set_pseudo(data['pseudo'])
            streak.set_streak(data['streak'])
            streak.set_date(data['date'])
            return jsonify(streak), 200
        else:
            return jsonify({"error": "Streak not found"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/streak/<int:streak_id>', methods=['DELETE'])
def delete_streak(streak_id):
    '''Delete a streak
    Return : {message} or {error}'''
    streak = Streak.get_streak_by_id(streak_id)
    if streak:
        streak.delete_streak()
        return jsonify({"message": "Streak deleted"}), 200
    else:
        return jsonify({"error": "Streak not found"}), 404

@app.route('/api/streak/<string:pseudo>', methods=['DELETE'])
def delete_streak_by_pseudo(pseudo):
    '''Delete a streak
    Return : {message} or {error}'''
    streak = Streak.get_streak_by_pseudo(pseudo)
    if streak:
        streak.delete_streak()
        return jsonify({"message": "Streak deleted"}), 200
    else:
        return jsonify({"error": "Streak not found"}), 404
'''END Streak API'''

'''Video API'''
@app.route('/api/video/<int:video_id>', methods=['GET'])
def get_video_by_id(video_id):
    '''Get a video by its ID
    Return : {id, title, description, link, image_link, upload_date} or {error}'''
    video = Video.get_video_by_id(video_id)
    if video:
        return jsonify(video), 200
    else:
        return jsonify({"error": "Video not found"}), 404

@app.route('/api/video', methods=['GET'])
def get_all_video():
    '''Get all videos
    Return : [video1, video2, ...]'''
    videos = Video.get_all_video()
    return jsonify(videos), 200

@app.route('/api/video', methods=['POST'])
def add_video():
    '''Add a video
    Request : {"title": "<TITLE>", "description": "<DESCRIPTION>", "link": "<LINK>", "image_link": "<IMAGE_LINK>", "upload_date": "<UPLOAD_DATE>"}
    Return : {id, title, description, link, image_link, upload_date} or {error}'''
    data = request.get_json()
    try:
        Video.add_video(data['title'], data['description'], data['link'], data['image_link'], data['upload_date'])
        return jsonify({"message": "Video added"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/video', methods=['PUT'])
def update_video():
    '''Update a video
    Request : {"id": 1, "title": "<TITLE>", "description": "<DESCRIPTION>", "link": "<LINK>", "image_link": "<IMAGE_LINK>", "upload_date": "<UPLOAD_DATE>"}
    Return : {id, title, description, link, image_link, upload_date} or {error}'''
    data = request.get_json()
    try:
        video = Video.get_video_by_id(data['id'])
        if video:
            video.set_title(data['title'])
            video.set_description(data['description'])
            video.set_link(data['link'])
            video.set_image_link(data['image_link'])
            video.set_upload_date(data['upload_date'])
            return jsonify(video), 200
        else:
            return jsonify({"error": "Video not found"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/video/<int:video_id>', methods=['DELETE'])
def delete_video(video_id):
    '''Delete a video
    Return : {message} or {error}'''
    video = Video.get_video_by_id(video_id)
    if video:
        video.delete_video()
        return jsonify({"message": "Video deleted"}), 200
    else:
        return jsonify({"error": "Video not found"}), 404
'''END Video API'''

'''Podcast API'''
@app.route('/api/podcast/<int:podcast_id>', methods=['GET'])
def get_podcast_by_id(podcast_id):
    '''Get a podcast by its ID
    Return : {id, title, description, link, image_link, upload_date} or {error}'''
    podcast = Podcast.get_podcast_by_id(podcast_id)
    if podcast:
        return jsonify(podcast), 200
    else:
        return jsonify({"error": "Podcast not found"}), 404

@app.route('/api/podcast', methods=['GET'])
def get_all_podcast():
    '''Get all podcasts
    Return : [podcast1, podcast2, ...]'''
    podcasts = Podcast.get_all_podcast()
    return jsonify(podcasts), 200

@app.route('/api/podcast', methods=['POST'])
def add_podcast():
    '''Add a podcast
    Request : {"title": "<TITLE>", "description": "<DESCRIPTION>", "link": "<LINK>", "image_link": "<IMAGE_LINK>", "upload_date": "<UPLOAD_DATE>"}
    Return : {id, title, description, link, image_link, upload_date} or {error}'''
    data = request.get_json()
    try:
        Podcast.add_podcast(data['title'], data['description'], data['link'], data['image_link'], data['upload_date'])
        return jsonify({"message": "Podcast added"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/podcast', methods=['PUT'])
def update_podcast():
    '''Update a podcast
    Request : {"id": 1, "title": "<TITLE>", "description": "<DESCRIPTION>", "link": "<LINK>", "image_link": "<IMAGE_LINK>", "upload_date": "<UPLOAD_DATE>"}
    Return : {id, title, description, link, image_link, upload_date} or {error}'''
    data = request.get_json()
    try:
        podcast = Podcast.get_podcast_by_id(data['id'])
        if podcast:
            podcast.set_title(data['title'])
            podcast.set_description(data['description'])
            podcast.set_link(data['link'])
            podcast.set_image_link(data['image_link'])
            podcast.set_upload_date(data['upload_date'])
            return jsonify(podcast), 200
        else:
            return jsonify({"error": "Podcast not found"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/podcast/<int:podcast_id>', methods=['DELETE'])
def delete_podcast(podcast_id):
    '''Delete a podcast
    Return : {message} or {error}'''
    podcast = Podcast.get_podcast_by_id(podcast_id)
    if podcast:
        podcast.delete_podcast()
        return jsonify({"message": "Podcast deleted"}), 200
    else:
        return jsonify({"error": "Podcast not found"}), 404
'''END Podcast API'''


if __name__ == '__main__':
    app.run(debug=True)