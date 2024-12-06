from backend.database.db_setup import db


class Video(db.Model):
    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    link = db.Column(db.String(255), nullable=True)
    image_link = db.Column(db.String(255), nullable=True)
    upload_date = db.Column(db.DateTime, nullable=False)

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

    def set_link(self, link):
        self.link = link
        db.session.commit()

    def set_description(self, description):
        self.description = description
        db.session.commit()

    def set_title(self, title):
        self.title = title
        db.session.commit()

    def set_image_link(self, image_link):
        self.image_link = image_link
        db.session.commit()

    def set_upload_date(self, upload_date):
        self.upload_date = upload_date
        db.session.commit()

    def delete_video(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_video():
        return [{'id':video.id, 'title':video.title, 'description':video.description, 'link':video.link, 'image_link':video.image_link, 'upload_date':video.upload_date} for video in Video.query.all()]

    @staticmethod
    def add_video(title, description, link, image_link, upload_date):
        new_video = Video(title=title, description=description, link=link,image_link=image_link,upload_date=upload_date)
        db.session.add(new_video)
        db.session.commit()


    @staticmethod
    def get_video_by_id(video_id):
        video = Video.query.get(video_id)
        if video:
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