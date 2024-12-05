from database.db_setup import db


class Video(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Enum('Humain', 'Océon', 'Les deux', name='answer_enum'), nullable=False)

    def __init__(self, title, description,link,image_link,upload_date):
        self.title = title
        self.description = description
        self.link = link
        self.image_link = image_link
        self.upload_date = upload_date

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_image_link(self):
        return self.image_link

    def get_image_image_link(self):
        return self.image_link

    def get_image_upload_date(self):
        return self.upload_date

    def set_link(self, question):
        self.link = link
        db.session.commit()

    def set_description(self, answer):
        self.description = description
        db.session.commit()

    def set_title(self, answer):
        self.title = title
        db.session.commit()

    def set_image_link(self, answer):
        self.image_link = image_link
        db.session.commit()

    def set_upload_date(self, answer):
        self.upload_date = upload_date
        db.session.commit()

    def delete_video(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_video():
        return [{'id':quiz.id, 'title':quiz.title, 'description':quiz.description, 'link':quiz.link, 'image_link':quiz.image_link, 'upload_date':quiz.upload_date} for quiz in Quiz.query.all()]

    @staticmethod
    def add_video(title, description, link, image_link, upload_date):
        new_video = Quiz(title=title, description=description, link=link,image_link=image_link,upload_date=upload_date)
        db.session.add(new_video)
        db.session.commit()


    @staticmethod
    def get_video_by_id(video_id):
        video = Video.query.get(video_id)
        if quiz:
            return {
                "id": video.id,
                "title": video.title,
                "description": video.description,
                "link": video.link,
                "image_link": video.image_link,
                "upload_date": video.upload_date,

            }
        else:
            return None