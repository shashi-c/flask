from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class StudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    qualification = StringField('Highest degree qualification', validators=[DataRequired()])
    passout = StringField('Passout year', validators=[DataRequired()])
    stream = StringField('Stream', validators=[DataRequired()])
    submit = SubmitField('Add')

class StudentSearchForm(FlaskForm):
    personalDetails = [('Name', 'name'),
                       ('Phone', 'phone'),
                       ('Email', 'email')
                      ]
    baseChoices = [('Qualification', 'qualification'),
                   ('Passout', 'passout')
                  ]
    advChoices = [('Stream', 'stream')]
                    
    selectStudent = SelectField('Student:', choices=personalDetails)
    selectBaseChoice = SelectField('Base:', choices=baseChoices)
    selectAdvChoice = SelectField('Advanced:', choices=advChoices)
    student = StringField('')
    base = StringField('')
    adv = StringField('')
