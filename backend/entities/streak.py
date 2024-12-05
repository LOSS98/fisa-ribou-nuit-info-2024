from backend.database.db_setup import db


class Quiz(db.Model):
    __tablename__ = 'streaks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pseudo = db.Column(db.String(255), nullable=False)
    streak = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)


    def __init__(self, pseudo, streak, date):
        self.pseudo = pseudo
        self.streak = streak
        self.date = date

    def get_pseudo(self):
        return  self.pseudo

    def get_streak(self):
        return self.streak

    def get_date(self):
        return self.date

    def set_pseudo(self, pseudo):
        self.pseudo = pseudo
        db.session.commit()

    def set_streak(self, streak):
        self.streak = streak
        db.session.commit()

    def set_date(self, date):
        self.date = date
        db.session.commit()

    def delete_streak(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_streaks():
        return [{'id':quiz.id, 'pseudo':quiz.pseudo, 'streak':quiz.streak, 'date':quiz.date} for quiz in Quiz.query.all()]

    @staticmethod
    def get_all_streak():
        return [{'id': quiz.id, 'pseudo': quiz.pseudo, 'streak': quiz.streak, 'date': quiz.date} for quiz in
                Quiz.query.order_by(Quiz.date).all()]

    @staticmethod
    def add_streak(pseudo, streak, date):
        new_quiz = Quiz(pseudo=pseudo, streak=streak, date=date)
        db.session.add(new_quiz)
        db.session.commit()

    @staticmethod
    def get_streak_by_id(streak_id):
        quiz = Quiz.query.order_by(Quiz.date).get(streak_id)
        if quiz:
            return {
                "id": quiz.id,
                "pseudo": quiz.pseudo,
                "streak": quiz.streak,
                "date": quiz.date
            }
        else:
            return None

    @staticmethod
    def get_streak_by_pseudo(pseudo):
        quiz = Quiz.query.order_by(Quiz.date).filter_by(pseudo=pseudo).first()
        if quiz:
            return {
                "id": quiz.id,
                "pseudo": quiz.pseudo,
                "streak": quiz.streak,
                "date": quiz.date
            }
        else:
            return None

    @staticmethod
    def get_streak_by_date(date):
        quiz = Quiz.query.order_by(Quiz.date).filter_by(date=date).first()
        if quiz:
            return {
                "id": quiz.id,
                "pseudo": quiz.pseudo,
                "streak": quiz.streak,
                "date": quiz.date
            }
        else:
            return None
