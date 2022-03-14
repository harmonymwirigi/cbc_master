import flask_bcrypt

from cbc.model import Teacher,teacher_learner,levels,Assignment,Assignment_material,Submission_material,Submission,Strand_materials,Sub_strand,Strands,Sub_strand_materials
from cbc.form import RegistrationForm,Login
from flask import render_template, url_for, redirect, flash
from flask_bcrypt import Bcrypt
from cbc import app,db

# landing page route
@app.route("/")
def land():
    form = RegistrationForm()
    return render_template('landing.html', form = form)

# teachers pannel
@app.route("/teachers")
def teachers():
    return render_template('teachers_pannel.html')

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
        return redirect(url_for('teachers'))

    # first_name = request.form.get('first_name')
    # last_name = request.form.get('last_name')
    # email = request.form.get('email')
    # phone_number = request.form.get('phone_number')
    # date = request.form.get('date')
    # gender = request.form.get('gender')
    # user_name = request.form.get('user_name')
    # password = request.form.get('password')
    # confirm_password = request.form.get('confirm_password')

    return render_template('landing.html', form = form)