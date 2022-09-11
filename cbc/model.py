from cbc import db, login_manager
from flask_login import UserMixin
from flask import session
import datetime


@login_manager.user_loader
def load_user(user_id):
    if 'user_type' in session:
        if session["user_type"] == "admin":
            return School.query.get(int(user_id))
        if session["user_type"] == "teacher":
            return Teacher.query.get(int(user_id))
        if session["user_type"] == "learner":
            return Learner.query.get(int(user_id))


class_learner = db.Table('class_learner',
                         db.Column('student_id', db.Integer, db.ForeignKey('learner.id')),
                         db.Column('class_id', db.Integer, db.ForeignKey('class.id'))
                         )
learner_assignment = db.Table('learner_assignment',
                              db.Column('student_id', db.Integer, db.ForeignKey('learner.id')),
                              db.Column('assignment_id', db.Integer, db.ForeignKey('assignment.id'))
                              )


class School(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    School_Name = db.Column(db.String(30), nullable=False)
    School_Email = db.Column(db.String(30), nullable=False)
    Password = db.Column(db.String(30), nullable=False)
    Confirm_Password = db.Column(db.String(30), nullable=False)
    Phone_Number = db.Column(db.String(30), nullable=False)
    type = db.Column(db.String, nullable=False)
    Students = db.relationship('Learner', backref='school', lazy=True)
    Teachers = db.relationship('Teacher', backref="school", lazy=True)
    levels = db.relationship('Level', backref='school', lazy=True)
    courses = db.relationship('Class', backref='school', lazy=True)
    code = db.Column(db.String(20), unique=True)


class Teacher(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    classes = db.relationship('Class', backref="teacher", lazy=True)
    password = db.Column(db.String(120), nullable=False)
    confirm_password = db.Column(db.String(120), nullable=False)
    my_school = db.Column(db.Integer, db.ForeignKey('school.id'))
    assignment = db.relationship('Assignment', backref = 'teacher', lazy = True)

    def __repr__(self):
        return f'{self.first_name}'


class Learner(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    second_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    reg_no = db.Column(db.String(20), nullable=False, unique=True, default=1)
    progress = db.Column(db.Integer, default=1)
    my_level = db.Column(db.Integer, db.ForeignKey('level.id'))
    pass_code = db.Column(db.String(120), nullable=False)
    my_course = db.relationship('Class', secondary=class_learner, backref="learners")
    my_school = db.Column(db.Integer, db.ForeignKey('school.id'))
    my_assignments = db.relationship('Assignment', secondary=learner_assignment, backref="learners")

    def __repr__(self):
        return f'<Level "{self.first_name}">'


class Class(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    className = db.Column(db.String(20), nullable=False)
    Teacher = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    my_level = db.Column(db.Integer, db.ForeignKey('level.id'))
    my_school = db.Column(db.Integer, db.ForeignKey('school.id'))
    assignments = db.relationship('Assignment', backref='course', lazy = True)

    def __repr__(self):
        return f'"{self.className}"'


class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20), nullable=False)
    classes = db.relationship('Class', backref='level', lazy=True)
    students = db.relationship('Learner', backref='level', lazy=True)
    my_school = db.Column(db.Integer, db.ForeignKey('school.id'))

    def __repr__(self):
        return '<Choice {}>'.format(self.Name)

    def __repr__(self):
        return f'{self.Name}'


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    my_course = db.Column(db.Integer, db.ForeignKey('class.id'))
    my_teacher = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    assignment_content = db.Column(db.Text, nullable=False)
    submited = db.relationship('SubmittedAssignment', backref = 'my_assignment', lazy = True)
    state = db.Column(db.Boolean, nullable=False, default=False)
    data = db.Column(db.LargeBinary, nullable=False)
    name = db.Column(db.String(30))


class SubmittedAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable = False)
    data = db.Column(db.LargeBinary, nullable = False)
    name = db.Column(db.String(30))
    assignment = db.Column(db.Integer, db.ForeignKey('assignment.id'))
    student = db.Column(db.Integer, db.ForeignKey('learner.id'))
    marks = db.Column(db.Integer, default = 0)



def is_active(self):
    return True
