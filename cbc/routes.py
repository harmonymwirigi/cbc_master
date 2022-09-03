import flask_bcrypt
from flask_login import login_user, current_user, logout_user, login_required

from cbc.model import School, Teacher, Learner, Level, Class
from cbc.form import RegistrationForm, Login, addStudent, removeStudent, Student_login, lessonPlan, CreateClass, \
    Student_signup, AddLevel, Teachers, Courses, Learners
from flask import render_template, url_for, flash, redirect, request, session
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


# schools account
@app.route("/school")
@login_required
def school():
    addForm = AddLevel()
    teacher_form = Teachers()
    learners = Learners()
    courses = Courses()
    learners.level.choices = [(level.Name) for level in
                              Level.query.filter_by(my_school=current_user.id).all()]
    courses.Teacher.choices = [(teacher.first_name) for teacher in
                               Teacher.query.filter_by(my_school=current_user.id).all()]
    courses.my_level.choices = [(course.Name) for course in
                                Level.query.filter_by(my_school=current_user.id).all()]
    classes = current_user.levels
    teachas = current_user.Teachers
    coursess = current_user.courses
    learner = current_user.Students
    return render_template('index.html', form=addForm, classes=classes, teacher_form=teacher_form, teachers=teachas,
                           cours=coursess,
                           courses=courses, no_of_teachers=len(teachas), no_of_classes=len(classes), learners=learners,
                           learner=learner, no_of_courses=len(coursess), no_of_learner=len(learner))


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
        schools = School.query.all()
        k = len(schools)+1
        hashed_passwed = flask_bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        school = School(School_Name=form.school_name.data, type=form.level.data, School_Email=form.email.data,
                        Phone_Number=form.phone_number.data, Password=hashed_passwed,
                        Confirm_Password=hashed_passwed, code =  "{:04d}".format(k))
        db.session.add(school)
        db.session.commit()
        print("{:04d}".format(school.id))
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
    if addForm.validate_on_submit():
        name1 = Level.query.filter_by(Name= addForm.name.data, my_school = current_user.id).first()
        if name1:
            flash(f"CLASS ALREADY EXIST", category="warning")
        else:
            clas = Level(Name=addForm.name.data, my_school=current_user.id)
            db.session.add(clas)
            db.session.commit()
            return redirect(url_for('levels'))
    return render_template('home/level.html', form = addForm)


@app.route("/cbc.com", methods=["POST", "GET"])
def TLearner():
    form2 = Student_login()
    if form2.validate_on_submit():
        teacher = Teacher.query.filter_by(email=form2.email.data).first()
        learner = Learner.query.filter_by(reg_no = form2.email.data).first()
        if teacher and bcrypt.check_password_hash(teacher.password, form2.password.data):
            session['user_type'] = 'teacher'
            login_user(teacher, remember=form2.remember.data)
            next_page = request.args.get('next')
            flash(f'LOGIN SUCCESS', category='success')
            return redirect(next_page) if next_page else redirect(url_for('Tlearn'))
        if learner and bcrypt.check_password_hash(learner.pass_code, form2.password.data):
            session['user_type'] = 'learner'
            login_user(learner, remember=form2.remember.data)
            next_page = request.args.get('next')
            flash(f'LOGIN SUCCESS', category='success')
            return redirect(next_page) if next_page else redirect(url_for('students'))
    return render_template('login.html', form2=form2)


@app.route("/school/teachers", methods=['POST'])
@login_required
def addTeacher():
    teacher_form = Teachers()
    addForm = AddLevel()
    courses = Courses()
    learners = Learners()
    if teacher_form.validate_on_submit():
        hashed_passwed = flask_bcrypt.generate_password_hash(teacher_form.Password.data).decode('utf-8')
        teacher1 = Teacher(first_name=teacher_form.Fname.data, last_name=teacher_form.Sname.data,
                           email=teacher_form.email.data,
                           phone_number=teacher_form.Phone_Number.data, password=hashed_passwed,
                           confirm_password=hashed_passwed, my_school=current_user.id)
        db.session.add(teacher1)
        db.session.commit()
        return redirect(url_for('school'))
    return render_template('index.html', teacher_form=teacher_form, form=addForm, courses=courses, learners=learners)


@app.route("/school/Courses", methods=['GET', 'POST'])
@login_required
def addCourses():
    teacher_form = Teachers()
    addForm = AddLevel()
    courses = Courses()
    learners = Learners()
    courses.Teacher.choices = [(teacher.first_name) for teacher in
                               Teacher.query.filter_by(my_school=current_user.id).all()]
    courses.my_level.choices = [(course.Name) for course in
                                Level.query.filter_by(my_school=current_user.id).all()]
    if courses.validate_on_submit():
        course1 = Level.query.filter_by(Name=courses.my_level.data, my_school = current_user.id).first()
        teacher1 = Teacher.query.filter_by(first_name=courses.Teacher.data, my_school = current_user.id).first()
        course = Class(className=courses.className.data, Teacher=teacher1.id, my_level=course1.id,
                       my_school=current_user.id)
        db.session.add(course)
        db.session.commit()
        students = Learner.query.filter_by(my_school=current_user.id).all()
        print(course, course.my_level, students)
        if students:
            for student in students:
                l = student.my_course
                for i in l:
                    c = Level.query.filter_by(id = i.my_level).first()
                    if c.Name == courses.my_level.data:
                        if course not in l:
                            student.my_course.append(course)
                            db.session.commit()
        return redirect(url_for('school'))
    return render_template('school.html', teacher_form=teacher_form, form=addForm, courses=courses, learners=learners)


@app.route("/school/learners", methods=['GET','POST'])
@login_required
def addLearner():
    learners = Learners()
    f = Learner.query.filter_by(my_school= current_user.id).all()
    reg_no = str(current_user.code) + "/" + str("{:04d}".format(len(f)+1))
    learners.level.choices = [(level.Name) for level in
                              Level.query.filter_by(my_school=current_user.id).all()]
    if learners.validate_on_submit():
        hashed_pass_code = flask_bcrypt.generate_password_hash(learners.pass_code.data).decode('utf-8')
        class1 = Level.query.filter_by(Name=learners.level.data).first()
        learners1 = Learner(first_name=learners.Fname.data, second_name=learners.Sname.data, email=learners.email.data,
                            reg_no= reg_no, my_level=class1.id, pass_code=hashed_pass_code,
                            my_school=current_user.id)
        courses = current_user.courses
        print(courses)
        db.session.add(learners1)
        db.session.commit()
        for i in courses:
            student_level = Level.query.filter_by(id = i.my_level).first()
            courses_level = Level.query.filter_by(id = learners1.my_level).first()
            print(i, i.my_level, learners1.my_level)
            if student_level.Name == courses_level.Name:
                learners1.my_course.append(i)
                db.session.commit()
        return redirect(url_for('school'))
    else:
        flash(f'please enter correct details', category='warning')
    return render_template('/home/students.html', learners=learners)


@app.route("/teachers")
@login_required
def tables():
    teacher_form = Teachers()
    teachas = current_user.Teachers
    return render_template('home/tables.html', teachers=teachas, teacher_form=teacher_form)


@app.route("/levels")
@login_required
def levels():
    addForm = AddLevel()
    classes = Level.query.filter_by(my_school = current_user.id).all()

    return render_template('home/level.html', form=addForm, classes=classes)


@app.route("/courses")
@login_required
def courses():
    addForm = AddLevel()
    courses = Courses()
    teachas = current_user.Teachers
    classes = current_user.levels
    coursess = current_user.courses
    courses.Teacher.choices = [(teacher.first_name) for teacher in
                               Teacher.query.filter_by(my_school=current_user.id).all()]
    courses.my_level.choices = [(course.Name) for course in
                                Level.query.filter_by(my_school=current_user.id).all()]
    return render_template("home/courses.html", teachers=teachas, form=addForm, classes=classes, courses=courses, cours=coursess)

@app.route("/students")
@login_required
def learners():
    learners = Learners()
    learners.level.choices = [(level.Name) for level in
                              Level.query.filter_by(my_school=current_user.id).all()]
    learner = current_user.Students
    for i in learner:
        print(len(i.my_course))
    return render_template("home/students.html", learners=learners, learner = learner)


@app.route("/teacher")
@login_required
def Tlearn():
    courses = Class.query.filter_by(Teacher = current_user.first_name).all()
    students = [(student.id) for student in Class.query.filter_by(Teacher=current_user.first_name).all()]
    learner = [(Learner.query.filter_by(id=i).first()) for i in students]
    return render_template("teachers-index.html", no_of_courses = len(courses), courses=courses,learner = learner)


@app.route("/teacher/courses")
@login_required
def Tcourses():
    courses = Class.query.filter_by(Teacher = current_user.first_name).all()
    return render_template("home/Tcourse.html", courses=courses)

@app.route("/teacher/students")
@login_required
def Tstudents():
    students = [(student.id) for student in Class.query.filter_by(Teacher = current_user.first_name).all()]
    learner = [(Learner.query.filter_by(id = i).first())for i in students]
    j = []
    for i in learner:
        j.append(i.id)
    courses = [(Class.query.filter_by(id = k).first())for k in j]
    print(courses)
    return render_template("home/Tstudents.html", learner = learner, courses = courses)


@app.route("/students/<user_id>")
@login_required
def profile(user_id):
    user1 = Learner.query.filter_by(id = user_id).first()
    return render_template("home/profile.html", user = user1)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('land'))


@app.route("/student")
@login_required
def students():
    return render_template('learner-index.html')
