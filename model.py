from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False) 
    url = db.Column(db.String, nullable=False, unique=True)
    published = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<News {self.title}, {self.url}>"
# UserMixin (is_authenticated)
class User(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True) # index служит для фильтрации запросов 
    password = db.Column(db.String(64))
    role = db.Column(db.String(10), index=True) 
    email = db.Column(db.String(50))


    # get password user and hash password
    def set_password(self, password):
        self.password = generate_password_hash(password)
    # get password of form user login and callate password hash with password hash database 
    def check_password(self, password):
        return check_password_hash(self.password, password)   

    @property # checks if the admin in the session routs admin
    def is_admin(self):
        return self.role == "admin" 


    def __repr__(self): 
        return f"<User: {self.username}>"