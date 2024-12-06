from backend.database.db_setup import db


class Streak(db.Model):
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
        return [{'id':streak.id, 'pseudo':streak.pseudo, 'streak':streak.streak, 'date':streak.date} for streak in Streak.query.all()]

    @staticmethod
    def get_all_streak():
        return [{'id': streak.id, 'pseudo': streak.pseudo, 'streak': streak.streak, 'date': streak.date} for streak in
                Streak.query.order_by(Streak.date).all()]

    @staticmethod
    def add_streak(pseudo, streak, date):
        new_streak = Streak(pseudo=pseudo, streak=streak, date=date)
        db.session.add(new_streak)
        db.session.commit()

    @staticmethod
    def get_streak_by_id(streak_id):
        streak = Streak.query.order_by(Streak.date).get(streak_id)
        if streak:
            return {
                "id": streak.id,
                "pseudo": streak.pseudo,
                "streak": streak.streak,
                "date": streak.date
            }
        else:
            return None

    @staticmethod
    def get_streak_by_pseudo(pseudo):
        streak = Streak.query.order_by(Streak.date).filter_by(pseudo=pseudo).first()
        if streak:
            return {
                "id": streak.id,
                "pseudo": streak.pseudo,
                "streak": streak.streak,
                "date": streak.date
            }
        else:
            return None

    @staticmethod
    def get_streak_by_date(date):
        streak = Streak.query.order_by(Streak.date).filter_by(date=date).first()
        if streak:
            return {
                "id": streak.id,
                "pseudo": streak.pseudo,
                "streak": streak.streak,
                "date": streak.date
            }
        else:
            return None
