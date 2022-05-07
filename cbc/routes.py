import flask_bcrypt
from flask_login import login_user, current_user, logout_user, login_required

from cbc.model import Teacher, teacher_learner, Learner, levels, Assignment, Assignment_material, Submission_material, Submission, Strand_materials, Sub_strand, Strands, Sub_strand_materials, Lessonplan
from cbc.form import RegistrationForm, Login, addStudent, removeStudent, Student_login, lessonPlan
from flask import render_template, url_for, flash, redirect, request
from flask_bcrypt import Bcrypt
from cbc import app, db, bcrypt


# landing page route
@app.route("/")
def land():
    form = RegistrationForm()
    form2 = Login()
    form_lesson_plan = lessonPlan()
    return render_template('landing.html', form=form, form2=form2, form_lesson = form_lesson_plan)


# teachers pannel
@app.route("/teachers")
@login_required
def teachers():
    formadd = addStudent()
    formremove = removeStudent()
    form_lesson_plan = lessonPlan()
    learners = Learner.query.order_by(Learner.id.asc()).all()
    lesson = Lessonplan.query.order_by(Lessonplan.id.asc()).all()
    return render_template('teachers_pannel.html', formadd=formadd, formremove=formremove, learners = learners, lesson = lesson, form_lesson = form_lesson_plan)


@app.route("/add", methods=["POST"])
@login_required
def add():
    formadd = addStudent()
    formremove = removeStudent()
    form_lesson_plan = lessonPlan()
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
    return render_template('teachers_pannel.html', formadd=formadd, formremove=formremove, form_lesson = form_lesson_plan)


@app.route("/remove", methods=["POST"])
@login_required
def remove():
    formremove = removeStudent()
    formadd = addStudent()
    form_lesson_plan = lessonPlan()
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
    return render_template('teachers_pannel.html', formremove=formremove, formadd=formadd, form_lesson = form_lesson_plan)
@app.route("/lessonplan", methods = ["POST"])
def lessonplan():
    form_lesson_plan = lessonPlan()
    formremove = removeStudent()
    formadd = addStudent()
    if form_lesson_plan.validate_on_submit():
        lesson = Lessonplan(grade = form_lesson_plan.grade.data, strands = form_lesson_plan.topic.data,
                            roll = form_lesson_plan.school.data, subStrand = form_lesson_plan.sub_strand.data, lesson_outcome = form_lesson_plan.learning_outcome.data,
                            core_comp = form_lesson_plan.core_competencies.data, values = form_lesson_plan.values.data, pci = form_lesson_plan.Pcis.data,
                            learning_material = form_lesson_plan.resources.data, introduction = form_lesson_plan.intro.data, LessonDev = form_lesson_plan.lesson_dev.data,
                            summary = form_lesson_plan.summary.data, conclusion = form_lesson_plan.conclusion.data)
        db.session.add(lesson)
        db.session.commit()
        flash(
            f' the lesson plan created successfully ',
            category="success")
        return redirect(url_for('teachers'))
    else:
        flash(f'please enter correct details', category='warning')
        return redirect(url_for('teachers'))
    return render_template('teachers_pannel.html', formremove=formremove, formadd=formadd, form_lesson = form_lesson_plan)


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
    form_lesson_plan = lessonPlan()
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
    return render_template('landing.html', form2=form2, form=form, form_lesson = form_lesson_plan)


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