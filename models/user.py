from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id, username="", email=""):
        self.id = id
        self.username = username
        self.email = email
    
    def set_username(self, username):
        self.username = username
        
    def set_email(self, email):
        self.email = email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)