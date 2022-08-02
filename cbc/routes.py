import flask_bcrypt
from flask_login import login_user, current_user, logout_user, login_required

from cbc.model import School, Teacher, Learner, Level, Class
from cbc.form import RegistrationForm, Login, addStudent, removeStudent, Student_login, lessonPlan, CreateClass, \
    Student_signup, AddLevel, Teachers, Courses
from flask import render_template, url_for, flash, redirect, request,session
from flask_bcrypt import Bcrypt
from cbc import app, db, bcrypt
from random import randint


# landing page route
@app.route("/", methods=['GET', 'POST'])
def land():
    form = RegistrationForm()
    formsignup = Student_signup()
    form2 = Login()
    form_lesson_plan = lessonPlan()
    return render_template('landing.html', form=form, form2=form2, form_lesson=form_lesson_plan, formsignup=formsignup)


# teachers pannel
@app.route("/teachers")
@login_required
def teachers():
    formadd = addStudent()
    learners = current_user.teaching
    teaching_courses = current_user.classes
    formremove = removeStudent()
    form_lesson_plan = lessonPlan()
    return render_template('teachers_pannel.html', formadd=formadd, learners=len(learners), formremove=formremove,
                           form_lesson=form_lesson_plan, teaching_courses = teaching_courses)


# schools account
@app.route("/school")
@login_required
def school():
    addForm = AddLevel()
    teacher_form = Teachers()
    courses = Courses()
    courses.Teacher.choices = [(teacher.first_name) for teacher in
                               Teacher.query.filter_by(my_school=current_user.id).all()]
    courses.my_level.choices = [(course.Name) for course in
                                Level.query.filter_by(my_school = current_user.id).all()]
    classes = current_user.levels
    teachas = current_user.Teachers
    coursess = current_user.courses
    return render_template('school.html', form=addForm,classes = classes, teacher_form=teacher_form, teachers=teachas, cours = coursess, courses = courses)


@app.route("/teachers/classes/createclass", methods=['POST'])
@login_required
def createClass():
    formadd = addStudent()
    classes = current_user.myClass
    formcreate = CreateClass()
    formremove = removeStudent()
    form_lesson_plan = lessonPlan()
    if formcreate.validate_on_submit():
        Classes = Class(className=formcreate.name.data, Teacher=current_user.id, level=formcreate.grade.data)
        db.session.add(Classes)
        db.session.commit()
        return redirect(url_for('classes'))
    return render_template('class.html', formcreate=formcreate,
                           formremove=formremove, form_lesson=form_lesson_plan,
                           classes=classes, formadd=formadd)


@app.route("/teachers/classes")
@login_required
def classes():
    classes = current_user.myClass
    formadd = addStudent()
    formremove = removeStudent()
    formcreate = CreateClass()
    form_lesson_plan = lessonPlan()
    return render_template('class.html', formcreate=formcreate,
                           formremove=formremove, form_lesson=form_lesson_plan,
                           classes=classes, formadd=formadd)


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
            return redirect(url_for('learners'))
        else:
            code = []
            for i in range(1, 5):
                n = randint(0, 9)
                code.append(n)
            cod = [str(item) for item in code]

            learner = Learner(email=formadd.email.data, grade=formadd.grade.data, first_name=formadd.first_name.data,
                              pass_code=int("".join(cod)),
                              second_name=formadd.second_name.data)

            db.session.add(learner)
            db.session.commit()
            current_user.teaching.append(learner)
            db.session.commit()
            email = request.form['email']
            flash(
                f'Account Created for {formadd.email.data} we have sent a verification email to {email} ',
                category="success")
            return redirect(url_for('learners'))
    else:
        flash(f'please enter correct details', category='warning')
        return redirect(url_for('learners'))
    return render_template('class.html', formadd=formadd, formremove=formremove, form_lesson=form_lesson_plan)


# @app.route("/teacher/class/<classId>")
# @login_required
# def  classDetails(classId):
#     clas = Class.query.filter_by(id= classId).first_or_404()
#     learners = current_user.teaching
#     lesson = Lessonplan.query.filter_by(teacher_id=current_user.id).all()
#     formremove = removeStudent()
#     formadd = addStudent()
#     form_lesson_plan = lessonPlan()
#     return render_template('class_details.html', student= clas, formadd=formadd, formremove=formremove,
#                            form_lesson=form_lesson_plan, learners=learners, lesson=lesson)


#  formremove=formremove, formadd=formadd, form_lesson = form_lesson_plan
@app.route("/remove/<studentId>")
def remove(studentId):
    student = Learner.query.filter_by(id=studentId).first()
    form_lesson_plan = lessonPlan()
    formremove = removeStudent()
    formadd = addStudent()
    db.session.delete(student)
    db.session.commit()
    flash("Student Remove successfully", 'success')
    return redirect(url_for('learners'))


#
# @app.route("/lessonplan", methods=["POST"])
# def lessonplan():
#     form_lesson_plan = lessonPlan()
#     formremove = removeStudent()
#     formadd = addStudent()
#     if form_lesson_plan.validate_on_submit():
#         lesson = Lessonplan(grade=form_lesson_plan.grade.data, teacher_id=current_user.id,
#                             strands=form_lesson_plan.topic.data,
#                             roll=form_lesson_plan.school.data, subStrand=form_lesson_plan.sub_strand.data,
#                             lesson_outcome=form_lesson_plan.learning_outcome.data,
#                             core_comp=form_lesson_plan.core_competencies.data, values=form_lesson_plan.values.data,
#                             pci=form_lesson_plan.Pcis.data,
#                             learning_material=form_lesson_plan.resources.data, introduction=form_lesson_plan.intro.data,
#                             LessonDev=form_lesson_plan.lesson_dev.data,
#                             summary=form_lesson_plan.summary.data, conclusion=form_lesson_plan.conclusion.data)
#         db.session.add(lesson)
#         db.session.commit()
#         flash(
#             f' the lesson plan created successfully ',
#             category="success")
#         return redirect(url_for('teachers'))
#     else:
#         flash(f'please enter correct details', category='warning')
#         return redirect(url_for('teachers'))
#     return render_template('teachers_pannel.html', formremove=formremove, formadd=formadd, form_lesson=form_lesson_plan, formsignup = formsignup)


# signup
@app.route("/signup", methods=["POST"])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_passwed = flask_bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        school = School(School_Name=form.school_name.data, type=form.level.data, School_Email=form.email.data,
                        Phone_Number=form.phone_number.data, Password=hashed_passwed,
                        Confirm_Password=hashed_passwed)
        db.session.add(school)
        db.session.commit()
        flash(f'you have created account successfully', category='success')
        return redirect(url_for('land'))

    return render_template('landing.html', form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    form2 = Login()
    form = RegistrationForm()
    if form2.validate_on_submit():
        user1 = School.query.filter_by(School_Email=form2.email.data).first()
        user2 = Teacher.query.filter_by(email=form2.email.data).first()
        if user1 and bcrypt.check_password_hash(user1.Password, form2.password.data):
            session['user_type'] = 'admin'
            login_user(user1, remember=form2.remember.data)
            next_page = request.args.get('next')
            flash(f'LOGIN SUCCESS', category='success')
            return redirect(next_page) if next_page else redirect(url_for('school'))
        else:
            flash(f'invalid email or password', category='error')

    else:
        flash(f'please enter correct details', category='warning')
    return render_template('landing.html', form2=form2, form=form)


@app.route("/school/add", methods=["POST"])
@login_required
def addlevel():
    addForm = AddLevel()
    teacher_form = Teachers()
    courses = Courses()
    if addForm.validate_on_submit():
        clas = Level(Name=addForm.name.data, my_school=current_user.id)
        db.session.add(clas)
        db.session.commit()
        return redirect(url_for('school'))
    else:
        flash(f'please enter correct details', category='warning')
    return render_template('school.html', form=addForm, teacher_form=teacher_form, courses = courses)


@app.route("/cbc.com", methods=["POST", "GET"])
def TLearner():
    form2 = Login()
    if form2.validate_on_submit():
        teacher = Teacher.query.filter_by(email=form2.email.data).first()
        if teacher and bcrypt.check_password_hash(teacher.password, form2.password.data):
            session['user_type'] = 'teacher'
            login_user(teacher, remember=form2.remember.data)
            next_page = request.args.get('next')
            flash(f'LOGIN SUCCESS', category='success')
            return redirect(next_page) if next_page else redirect(url_for('Tlearn'))
    return render_template('login.html', form2=form2)


@app.route("/school/teachers", methods=['POST'])
@login_required
def addTeacher():
    teacher_form = Teachers()
    addForm = AddLevel()
    courses = Courses()
    if teacher_form.validate_on_submit():
        hashed_passwed = flask_bcrypt.generate_password_hash(teacher_form.Password.data).decode('utf-8')
        teacher1 = Teacher(first_name=teacher_form.Fname.data, last_name=teacher_form.Sname.data,
                           email=teacher_form.email.data,
                           phone_number=teacher_form.Phone_Number.data, password=hashed_passwed,
                           confirm_password= hashed_passwed, my_school=current_user.id)
        db.session.add(teacher1)
        db.session.commit()
        return redirect(url_for('school'))
    return render_template('school.html', teacher_form=teacher_form, form=addForm, courses = courses)
@app.route("/school/Courses", methods = ['GET', 'POST'])
@login_required
def addCourses():
    teacher_form = Teachers()
    addForm = AddLevel()
    courses = Courses()
    courses.Teacher.choices = [(teacher.first_name) for teacher in
                               Teacher.query.filter_by(my_school=current_user.id).all()]
    courses.my_level.choices = [(course.Name) for course in
                                Level.query.filter_by(my_school=current_user.id).all()]
    if courses.validate_on_submit():
        course1 = Level.query.filter_by(Name = courses.my_level.data).first()
        teacher1 = Teacher.query.filter_by(first_name = courses.Teacher.data).first()
        course = Class(className = courses.className.data, Teacher = teacher1.first_name, my_level = course1.Name, my_school = current_user.id)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('school'))
    return render_template('school.html',teacher_form=teacher_form, form=addForm, courses = courses)

@app.route("/teacher")
@login_required
def Tlearn():
    teaching_courses = current_user.classes
    return render_template("teacher.html", teaching_courses = teaching_courses)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('land'))


@app.route("/student")
def students():
    form2 = Login()
    form = RegistrationForm()
    formsignup = Student_signup()
    return render_template('student_pannel.html', form2=form2, form=form, formsignup=formsignup)
