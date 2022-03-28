import flask_bcrypt
from flask_login import login_user, current_user, logout_user, login_required

from cbc.model import Teacher,teacher_learner,Learner,levels,Assignment,Assignment_material,Submission_material,Submission,Strand_materials,Sub_strand,Strands,Sub_strand_materials
from cbc.form import RegistrationForm,Login, addStudent, removeStudent
from flask import render_template, url_for, flash, redirect, request
from flask_bcrypt import Bcrypt
from cbc import app,db, bcrypt
# landing page route
@app.route("/")
def land():
    form = RegistrationForm()
    form2 = Login()
    return render_template('landing.html', form = form, form2 = form2)

# teachers pannel
@app.route("/teachers")
@login_required
def teachers():
    formadd = addStudent()
    formremove = removeStudent()
    return render_template('teachers_pannel.html', formadd = formadd, formremove =formremove)
@app.route("/add", methods = ["POST"])
@login_required
def add():
    formadd = addStudent()
    if formadd.validate_on_submit():
        learner = Learner(email = formadd.email.data, grade = formadd.grade.data, first_name = formadd.first_name.data, second_name = formadd.second_name.data)
        db.session.add(learner)
        db.session.commit()
        flash('Email sent successfully')
        return redirect(url_for('teachers'))
    return redirect('teachers_pannel.html', formadd = formadd)
@app.route("/remove", methods = ["POST"])
@login_required
def remove():
    formremove = removeStudent()
    if formremove.validate_on_submit():
        learner = Learner.query.filter_by(email=formremove.email.data).first()
        db.session.delete(learner)
        db.session.commit()
        flash('The student has been removed successfully')
        return redirect(url_for('teachers'))
    return redirect('teachers_pannel.html', formremove = formremove)

# signup
@app.route("/signup", methods = ["POST"])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_passwed = flask_bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        teacher = Teacher(first_name=form.first_name.data,last_name=form.last_name.data,email=form.email.data,
                          phone_number=form.phone_number.data,gender=form.gender.data,
                          user_name=form.user_name.data,password=hashed_passwed, confirm_password=form.confirm_password.data)
        db.session.add(teacher)
        db.session.commit()
        flash('you have created account succcessfully')
        return redirect(url_for('land'))

    return render_template('landing.html', form = form)
@app.route("/login", methods = ["POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('teachers'))
    form2 = Login()
    form = RegistrationForm()
    if form2.validate_on_submit():
        user = Teacher.query.filter_by(email=form2.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form2.password.data):
            login_user(user,remember=form2.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('teachers'))
    return render_template('landing.html', form2=form2, form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('land'))
