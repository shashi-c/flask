from app.constants import STUDENT
from .. import db


class UserRoles(db.Model):
    __tablename__ = "user_roles"

    role = db.Column(db.String(50), primary_key=True)

class Ticket(db.Model):
    """ Ticket Model for storing ticket related details """
    __tablename__ = "ticket"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    comments = db.relationship("Comment")

    def __repr__(self):
        return "<Ticket '{}'>".format(self.title)


class UserTickets(db.Model):
    __tablename__ = "user_tickets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(
        db.String(20),
        db.ForeignKey("user_roles.role"),
        default=STUDENT,
        nullable=False,
    )
    ticket_id = db.Column(db.Integer, db.ForeignKey("ticket.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Comment(db.Model):
    """Comment class which contains all comments for a ticket"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey("ticket.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    text = db.Column(db.String(2000), nullable=False)

