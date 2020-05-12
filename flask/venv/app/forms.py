from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DecimalField, IntegerField
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
    full_name = StringField('Full name', validators=[DataRequired()])
    active_year = StringField('Year of Joining KSV', validators=[DataRequired()])
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

class AuthorizationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Authorize')

class StudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    perm_addr = StringField('Permanent address', validators=[DataRequired()])

    qualification = StringField('Highest degree qualification', validators=[DataRequired()])
    passout = StringField('Passout year', validators=[DataRequired()])
    stream = StringField('Stream', validators=[DataRequired()])
    college = StringField('College', validators=[DataRequired()])

    tenth_percent = DecimalField('10th Percentage')
    plus2_percent = DecimalField('12th Percentage')
    degree_percent = DecimalField('Degree Percentage')
    n_backlogs = IntegerField('Total Backlogs if any')

    courses = StringField('Courses completed')
    skills = StringField('Skills', validators=[DataRequired()])

    hobbies = StringField('Hobbies')

    submit = SubmitField('Add')

class StudentSearchForm(FlaskForm):
    personalChoices = [('name', 'Name'),
                       ('phone', 'Phone'),
                       ('email', 'Email'),
                       ('address', 'Address')
                      ]
    academicChoices = [('qualification', 'Qualification'),
                       ('passout', 'Passout'),
                       ('stream', 'Stream'),
                       ('college', 'College')
                      ]

    gradeChoices = [('degree_percent', 'Degree average Percentage'),
                    ('n_backlogs', 'Number of Backlogs')
                   ]
                   # Irrelevent as of now
                   # ('tenth_percent', '10th Percentage'),
                   # ('plus2_percent', '12th Percentage'),

                    
    personalChoice = SelectField('Personal Details:', choices=personalChoices)
    academicChoice = SelectField('Academic Details:', choices=academicChoices)
    gradeChoice = SelectField('Grade Details:', choices=gradeChoices)

    personal = StringField('')
    academic = StringField('')
    grade = StringField('')
    courses = StringField('Courses')
    skills = StringField('Skills')


