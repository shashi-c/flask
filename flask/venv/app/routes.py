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
from app.forms import StudentSearchForm

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
                 user.student.name = form.name.data
            if form.email:
                user.student.email = form.email.data
            if form.phone:
                user.student.phone = form.phone.data
            if form.qualification:
                user.student.qualification = form.qualification.data
            if form.passout:
                user.student.passout = form.passout.data
            if form.stream:
                user.student.stream = form.stream.data
        else:
            db.session.add(student)
        db.session.commit()
        flash('**** Congratulations, your details have been added! ****')
        return redirect(url_for('index'))
    return render_template('student-details.html', title='Add Details', form=form)


@app.route('/show-details', methods=['GET', 'POST'])
@login_required
def show_details():
    print(current_user.student)
    result = []
    if current_user.student is None:
        flash('Nothing to show, Add your details first!!')
        return render_template('index.html', title='Home', user=current_user, student=current_user.student)
    else:
        result.append(current_user.student)
        table = StudentTable(result)
        table.border = True
        return render_template('show-details.html', title='Your Details', table=table)



@app.route('/show-all', methods=['GET', 'POST'])
@login_required
def show_all():
    if current_user.admin == False:
        return redirect(url_for('index'))
    students = []
    users = User.query.all()
    for u in users:
        if u.admin == False:
            students.append(u.student)

    for s in students:
        print(s.name, s.email)
    return render_template('show-all.html', students=students)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search_student():
    if current_user.admin == False:
        return redirect(url_for('index'))
    search = StudentSearchForm(request.form)
    print(search)
    if request.method == 'POST':
        return search_results(search)
    print('render template')
    return render_template('search.html', form = search)

@app.route('/results')
@login_required
def search_results(search):
    print('searching !!! ')
    if current_user.admin == False:
        return redirect(url_for('index'))
    results = []

    studentSearchStr = search.data['student']
    qry=db.session.query(Student)
    if studentSearchStr:
        if search.data['selectStudent'] == 'Name':
            qry = db.session.query(Student).filter(Student.name == studentSearchStr)
        elif search.data['selectStudent'] == 'Email':
            qry = db.session.query(Student).filter(Student.email == studentSearchStr)
        elif search.data['selectStudent'] == 'Phone':
            qry = db.session.query(Student).filter(Student.phone == studentSearchStr)
    baseSearchStr = search.data['base']
    if baseSearchStr:
        if search.data['selectBaseChoice'] == 'Qualification':
            if not qry.all() and not sudentSearchStr:
                qry = db.session.query(Student).filter(Student.qualification == baseSearchStr)
            else:
                qry = qry.filter(Student.qualification == baseSearchStr)
        if search.data['selectBaseChoice'] == 'Passout':
            if not qry.all() and not sudentSearchStr:
                qry = db.session.query(Student).filter(Student.passout == baseSearchStr)
            else:
                qry = qry.filter(Student.passout == baseSearchStr)
    advSearchStr = search.data['adv']
    if advSearchStr:
        if search.data['selectAdvChoice'] == 'Stream':
            if not qry.all() and not studentSearchStr and not advSearchStr:
                qry = db.session.query(Student).filter(Student.stream == advSearchStr)
            else:
                qry = qry.filter(Student.stream == advSearchStr)


    for item in qry.all():
        results.append(item)
    print(results)
    table = StudentTable(results)
    table.border = True
    return render_template('results.html', table=table)
