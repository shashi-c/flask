from flask import render_template
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User
from app.models import Student
from app.models import StudentTable
from flask_login import logout_user
from flask_login import login_required
from flask import request, redirect, url_for, flash
from werkzeug.urls import url_parse
from app import db
from sqlalchemy import update
from app.forms import RegistrationForm
from app.forms import StudentForm

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home', user=current_user, student=current_user.student)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.set_admin()
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/add-details', methods=['GET', 'POST'])
@login_required
def add_details():
    print("In add_details")
    form = StudentForm()
    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        student = Student(name = form.name.data,
                    email = form.email.data,
                    phone = form.phone.data,
                    qualification = form.qualification.data,
                    passout = form.passout.data,
                    stream = form.stream.data,
                    user=user)

        if user.student:
            if form.name:
                 user.student[0].name = form.name.data
            if form.email:
                user.student[0].email = form.email.data
            if form.phone:
                user.student[0].phone = form.phone.data
            if form.qualification:
                user.student[0].qualification = form.qualification.data
            if form.passout:
                user.student[0].passout = form.passout.data
            if form.stream:
                user.student[0].stream = form.stream.data
        else:
            db.session.add(student)
        db.session.commit()
        flash('**** Congratulations, your details have been added! ****')
        return redirect(url_for('index'))
    return render_template('student-details.html', title='Add Details', form=form)


@app.route('/show-details', methods=['GET', 'POST'])
@login_required
def show_details():
    user = User.query.get(current_user.id)
    student = user.student.all()
    print(student)
    if not student:
        flash('Nothing to show, Add your details first!!')
        return render_template('index.html', title='Home', user=current_user, student=current_user.student)
    return render_template('show-details.html', title='Your Details', student=student[0])



@app.route('/show-all', methods=['GET', 'POST'])
@login_required
def show_all():
    if current_user.admin == False:
        return redirect(url_for('index'))
    students = []
    users = User.query.all()
    for u in users:
        if u.admin == False or u.admin == None:
            student = u.student.all()
            students.append(student[0])

    for s in students:
        print(s.name, s.email)
    #s_t = StudentTable(students)
    #print(s_t.__html__())
    #return render_template('show-details.html', title='Your Details', student=student[0])
    return render_template('show-all.html', students=students)
