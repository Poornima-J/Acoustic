from app import login
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(64), index=True, unique=True)
    email=db.Column(db.String(120), index=True, unique=True)
    password_hash=db.Column(db.String(128))
    FileContents=db.relationship('FileContents',backref='user',lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self,password):
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

class FileContents(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(300))
    timestamp=db.Column(db.DateTime, index=True, default=datetime.utcnow)
    data=db.Column(db.LargeBinary)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Video {}>'.format(self.name)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
