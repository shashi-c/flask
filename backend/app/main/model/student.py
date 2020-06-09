
from .. import db

class Student(db.Model):
    """ User Model for storing student related details """
    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    college = db.Column(db.String(100))
    pass_out_year = db.Column(db.Integer)
    stream = db.Column(db.String(100))
    highest_degree = db.COlumn(db.String(100))

    def __repr__(self):
        return "<Student '{}'>".format(self.username)
