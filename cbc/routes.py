import flask_bcrypt
from flask_login import login_user, current_user, logout_user, login_required

from cbc.model import Teacher, teacher_learner, Learner, levels, Assignment, Assignment_material, Submission_material, \
    Submission, Strand_materials, Sub_strand, Strands, Sub_strand_materials
from cbc.form import RegistrationForm, Login, addStudent, removeStudent, Student_login
from flask import render_template, url_for, flash, redirect, request
from flask_bcrypt import Bcrypt
from cbc import app, db, bcrypt


# landing page route
@app.route("/")
def land():
    form = RegistrationForm()
    form2 = Login()
    return render_template('landing.html', form=form, form2=form2)


# teachers pannel
@app.route("/teachers")
@login_required
def teachers():
    formadd = addStudent()
    formremove = removeStudent()
    learners = Learner.query.order_by(Learner.id.asc()).all()
    return render_template('teachers_pannel.html', formadd=formadd, formremove=formremove, learners = learners)


@app.route("/add", methods=["POST"])
@login_required
def add():
    formadd = addStudent()
    formremove = removeStudent()
    if formadd.validate_on_submit():
        user = Learner.query.filter_by(email=formadd.email.data).first()
        if user:
            flash(f'the student exist', category='error')
            return redirect(url_for('teachers'))
        else:
            learner = Learner(email=formadd.email.data, grade=formadd.grade.data, first_name=formadd.first_name.data,
                              second_name=formadd.second_name.data)
            db.session.add(learner)
            db.session.commit()
            email = request.form['email']
            flash(
                f'Account Created for {formadd.email.data} we have sent a verification email to {email} ',
                category="success")
            return redirect(url_for('teachers'))
    else:
        flash(f'please enter correct details', category='warning')
        return redirect(url_for('teachers'))
    return render_template('teachers_pannel.html', formadd=formadd, formremove=formremove)


@app.route("/remove", methods=["POST"])
@login_required
def remove():
    formremove = removeStudent()
    formadd = addStudent()
    if formremove.validate_on_submit():
        user = Learner.query.filter_by(email=formremove.email.data).first()
        if user:
            learner = Learner.query.filter_by(email=formremove.email.data).first()
            db.session.delete(learner)
            db.session.commit()
            flash(f'The student has been removed successfully', category='success')
            return redirect(url_for('teachers'))
        else:
            flash(f'the student does not exist', category='error')
            return redirect(url_for('teachers'))
    else:
        flash(f'please enter correct details', category='warning')
        return redirect(url_for('teachers'))
    return render_template('teachers_pannel.html', formremove=formremove, formadd=formadd)


# signup
@app.route("/signup", methods=["POST"])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_passwed = flask_bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        teacher = Teacher(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                          phone_number=form.phone_number.data, gender=form.gender.data,
                          user_name=form.user_name.data, password=hashed_passwed,
                          confirm_password=form.confirm_password.data)
        db.session.add(teacher)
        db.session.commit()
        flash(f'you have created account successfully', category='success')
        return redirect(url_for('land'))

    return render_template('landing.html', form=form)


@app.route("/login", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('teachers'))
    form2 = Login()
    form = RegistrationForm()
    if form2.validate_on_submit():
        user = Teacher.query.filter_by(email=form2.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form2.password.data):
            flash(f'login successful', category='success')
            login_user(user, remember=form2.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('teachers'))
        else:
            flash(f'invalid email or password', category='error')

    else:
        flash(f'please enter correct details', category='warning')
    return render_template('landing.html', form2=form2, form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('land'))

@app.route("/student")
def students():
    form = Student_login()
    if form.validate_on_submit():
        email = form.email.data()
        password = form.password.data()
    return render_template('students_account.html', form = form)