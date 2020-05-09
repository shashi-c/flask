from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app import login
from flask_login import UserMixin
from flask_table import Table, Col

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean())
    student = db.relationship('Student', backref='user', uselist=False)

    def __repr__(self):
        return '<User {}>'.format(self.username) 


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_admin(self):
        if self.username == 'admin':
            self.admin = True
        else:
            self.admin = False

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    email = db.Column(db.String(140))
    phone = db.Column(db.String(15))
    perm_addr = db.Column(db.String(500))

    qualification = db.Column(db.String(140))
    passout = db.Column(db.String(10))
    stream = db.Column(db.String(50))
    college = db.Column(db.String(500))

    tenth_percent = db.Column(db.Float()) #U may add precession later
    plus2_percent = db.Column(db.Float())
    degree_percent = db.Column(db.Float())
    n_backlogs = db.Column(db.Integer)

    courses = db.Column(db.String(1024)) # Expect it to be comma seperated in input
    skills = db.Column(db.String(2048)) # Find text based search for this field

    hobbies = db.Column(db.String(1024))


    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

    def __repr__(self):
        return '<Student {}>'.format(self.name)

class StudentTable(Table):
    name = Col('Name')
    email = Col('Email')
    phone = Col('Phone')
    perm_addr = Col('Address')

    qualification = Col('Qualification')
    passout = Col('Passout')
    stream = Col('Stream')
    college = Col('College')

    tenth_percent = Col('10th Percent')
    plus2_percent = Col('12th Percent')
    degree_percent = Col('degree Percent')
    n_backlogs = Col('Backlogs')

    courses = Col('Courses')
    skills = Col('Skills')

    hobbies = Col('Hobbies')

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
