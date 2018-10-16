from flask_sqlalchemy import SQLAlchemy

from app import app

db = SQLAlchemy(app)

class DB_User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    passwd =  db.Column(db.String(64))
    token = db.Column(db.String(64))
    signature = db.Column(db.String(64))

class DB_Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    passwd =  db.Column(db.String(64))
    token = db.Column(db.String(64))
    flag = db.Column(db.String(64))
    signature = db.Column(db.String(64))


class User:
    def __init__(self,username):
        self.username = DB_User.query.filter_by(name=username).first().name
        self.token = DB_User.query.filter_by(name=username).first().token
        self.signature = DB_User.query.filter_by(name=username).first().signature
    # For Test
    def showsign(self):
        return self.signature

class Admin:
    def __init__(self,username='LiUU'):
        self.username = DB_Admin.query.filter_by(name=username).first().name
        self.token = DB_Admin.query.filter_by(name=username).first().token
        self.signature = DB_Admin.query.filter_by(name=username).first().signature + DB_Admin.query.filter_by(name=username).first().flag

class Users:


    def __init__(self,isadmin,username):
        self.username = username
        self.isadmin = isadmin
        self.user_admin = Admin()
        self.user_user = User(self.username)
        if(self.isadmin):
            self.user = self.user_admin
        else:
            self.user = self.user_user

