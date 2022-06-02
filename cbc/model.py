from cbc import db, login_manager
from flask_login import UserMixin
import datetime


@login_manager.user_loader
def load_user(user_email):
    return Teacher.query.get(int(user_email))


teacher_learner = db.Table('teacher_learner',
                           db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id')),
                           db.Column('learner_id', db.Integer, db.ForeignKey('learner.id'))
                           )

class_learner = db.Table('class_learner',
                         db.Column('student_id', db.Integer, db.ForeignKey('learner.id')),
                         db.Column('class_id', db.Integer, db.ForeignKey('class.id'))
                         )


class Teacher(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    user_name = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(120), nullable=False)
    confirm_password = db.Column(db.String(120), nullable=False)
    assignments = db.relationship('Assignment', backref='assignments', lazy=True)
    myClass = db.relationship('Class', backref='class', lazy=True)
    teaching = db.relationship('Learner', secondary=teacher_learner, backref="teachers")

    def __repr__(self):
        return f"Teacher('{Teacher.first_name}','{Teacher.email}','{Teacher.first_name}'"

class Learner(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    second_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    user_name = db.Column(db.String(40), unique=True)
    progress = db.Column(db.Integer, default=1)
    grade = db.Column(db.Integer, db.ForeignKey('levels.id'))
    password = db.Column(db.String(120), nullable=False)
    confirm_password = db.Column(db.String(120), nullable=False)
    submitted_assignment = db.relationship('Submission', backref="my_submission", lazy=True)


class Class(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    className = db.Column(db.String(20), nullable=False)
    Teacher = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    level = db.Column(db.String(30), nullable = False)
    myStudents = db.relationship('Learner', secondary = class_learner, backref = "learners")


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    sub_strand = db.Column(db.Integer, db.ForeignKey('sub_strand.id'))
    assignment_content = db.Column(db.Text, nullable=False)
    state = db.Column(db.Boolean, nullable=False, default=False)
    submission = db.relationship('Submission', backref="submission")
    materials = db.relationship('Assignment_material', backref="my_materials", lazy=True)


class Assignment_material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment = db.Column(db.Integer, db.ForeignKey('assignment.id'))
    material_file = db.Column(db.String(200), nullable=False)
    material_video = db.Column(db.String(200), nullable=False)
    material_picture = db.Column(db.String(200), nullable=False)


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marks = db.Column(db.String(20))
    assignment = db.Column(db.Integer, db.ForeignKey('assignment.id'))
    student = db.Column(db.Integer, db.ForeignKey('learner.id'))
    materials = db.relationship('Submission_material', backref="my_materials", lazy=True)


class Submission_material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    submission = db.Column(db.Integer, db.ForeignKey('submission.id'))
    material_text = db.Column(db.Text, nullable=False)
    material_file = db.Column(db.String(200), nullable=False)
    material_video = db.Column(db.String(200), nullable=False)
    material_picture = db.Column(db.String(200), nullable=False)


class levels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level_name = db.Column(db.String(20), unique=True)
    lessonPlan = db.Column(db.Integer, db.ForeignKey('lessonplan.id'))
    strands = db.relationship('Strands', backref="my_topics", lazy=True)
    students = db.relationship('Learner', backref="my_learners", lazy=True)


class Strands(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    grade_id = db.Column(db.Integer, db.ForeignKey('levels.id'))
    sub_strand = db.relationship('Sub_strand', backref="my_sub_strands", lazy=True)
    materials = db.relationship('Strand_materials', backref="my_materials", lazy=True)


class Strand_materials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strand = db.Column(db.Integer, db.ForeignKey('strands.id'))
    text = db.Column(db.Text, nullable=True)
    file = db.Column(db.Text, nullable=True)
    video = db.Column(db.Text, nullable=True)
    picture = db.Column(db.Text, nullable=True)


class Sub_strand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    strand = db.Column(db.Integer, db.ForeignKey('strands.id'))
    materials = db.relationship('Sub_strand_materials', backref="my_materials", lazy=True)
    assignment = db.relationship('Assignment', backref="my_assignments", lazy=True)


class Sub_strand_materials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_strand = db.Column(db.Integer, db.ForeignKey('sub_strand.id'))
    material_text = db.Column(db.Text, nullable=False)
    material_file = db.Column(db.String(200), nullable=False)
    material_video = db.Column(db.String(200), nullable=False)
    material_picture = db.Column(db.String(200), nullable=False)


class Lessonplan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.id"), nullable=False)
    grade = db.Column(db.String(30), nullable=False)
    strands = db.Column(db.String(200), nullable=False)
    roll = db.Column(db.Integer)
    subStrand = db.Column(db.String(200), nullable=False)
    lesson_outcome = db.Column(db.String(500), nullable=False)
    core_comp = db.Column(db.String(250), nullable=False)
    values = db.Column(db.String(230), nullable=False)
    pci = db.Column(db.String(300), nullable=False)
    learning_material = db.Column(db.String(300), nullable=False)
    introduction = db.Column(db.String(500), nullable=False)
    LessonDev = db.Column(db.String(1000), nullable=False)
    summary = db.Column(db.String(1000), nullable=False)
    conclusion = db.Column(db.String(1000), nullable=False)


def is_active(self):
    return True
