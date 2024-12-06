from backend.database.db_setup import db
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


    def __init__(self, email, password):
        self.email = email
        self.set_password(password)


    def get_email(self):
        return  self.email

    def get_password(self):
        return self.password

    def set_email(self, email):
        self.email = email
        db.session.commit()

    def set_password(self, password):
        """
        Hash le mot de passe avant de le stocker.
        """
        self.password = generate_password_hash(password)
        db.session.commit()

    @staticmethod
    def check_password(passwordToTest, password):
        """
        Valide un mot de passe donné contre le hash stocké.
        """
        #return check_password_hash(password, passwordToTest)

        return check_password_hash(password, passwordToTest)


    @staticmethod
    def get_all_email():
        return [{"Id": admin.id, "Email": admin.email, "Password": admin.password} for admin in Admin.query.all()]

    @staticmethod
    def get_admin_by_id(id):
        admin = Admin.query.get(id)
        if admin:
            return {"id": admin.id, "email": admin.email, "password": admin.password}
        else:
            return None

    @staticmethod
    def get_admin_by_email(email):
        """
        Récupère un administrateur par son email.
        Retourne un dictionnaire avec ses informations ou None si l'email n'existe pas.
        """
        admin = Admin.query.filter_by(email=email).first()
        if admin:
            return {"id": admin.id, "email": admin.email, "password": admin.password}
        return None


    def delete_admin(admin_id):
        """
        Supprime un admin de la base de données en fonction de son ID.
        """
        admin = Admin.query.get(admin_id)  # Récupère l'admin par son ID
        if admin:
            db.session.delete(admin)  # Supprime l'admin
            db.session.commit()  # Enregistre les modifications
            return {"message": f"L'admin avec l'ID {admin_id} a été supprimé avec succès."}
        else:
            return {"error": f"L'admin avec l'ID {admin_id} n'existe pas."}