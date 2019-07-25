from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app import login_manager
from flask_login import UserMixin
import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    tasks = db.relationship('Task', backref='person', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    upload = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    csv_file = db.Column(db.String(128), default=None)
    zip_file = db.Column(db.String(128), default=None)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))