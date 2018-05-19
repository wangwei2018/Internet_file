from app import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

class User(db.Model,UserMixin):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(20),nullable=False)
    password=db.Column(db.String(150),nullable=False)
    password_hash=db.Column(db.String(200))
    name=db.Column(db.String(20))
    sex=db.Column(db.Boolean)
    email=db.Column(db.String(20))
    info=db.Column(db.Text)
    memos=db.relationship("Memo",backref="user")
    receive_messages=db.relationship("Message",backref="receiver")
    files=db.relationship("File",backref="sender")


    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

class Memo(db.Model):
    __tablename__="memoes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    theme=db.Column(db.String(50),nullable=False)
    content = db.Column(db.Text,nullable=False)
    time = db.Column(db.String(20), nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"))

class Message(db.Model):
    __tablename__="messages"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender=db.Column(db.String(20),nullable=False)
    receiver_id=db.Column(db.Integer,db.ForeignKey("users.id"))
    content = db.Column(db.Text,nullable=False)
    time = db.Column(db.String(20), nullable=False)

class File(db.Model):
    __tablename__="files"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    filename=db.Column(db.String(50),nullable=False)
    filesize=db.Column(db.Float,nullable=False)
    time = db.Column(db.String(20), nullable=False)
    share=db.Column(db.Boolean,nullable=False)


from . import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
