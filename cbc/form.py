from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, BooleanField, DateTimeField, \
    TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from cbc.model import Level


class RegistrationForm(FlaskForm):
    school_name = StringField('SCHOOL NAME', validators=[DataRequired()])
    level = SelectField('LEVEL', validators=[DataRequired()], choices=[('MIDDLE LEVEL'), ('SENIOR LEVEL')])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=23)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class Login(FlaskForm):
    email = StringField('Enter School Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class Teachers(FlaskForm):
    Fname = StringField('First Name', validators=[DataRequired()])
    Sname = StringField('Second Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    Phone_Number = StringField('Phone', validators=[DataRequired()])
    Password = PasswordField('Password', validators=[DataRequired()])
    Confirm_Password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('Password')])
    submit = SubmitField('ADD')


class Learners(FlaskForm):
    Fname = StringField('FIRST NAME', validators=[DataRequired()])
    Sname = StringField('SECOND NAME', validators=[DataRequired()])
    email = StringField('NEXT OF KIN EMAIL', validators=[DataRequired(), Email()])
    level = SelectField('LEVEL', validators=[DataRequired()], choices=[])
    pass_code = PasswordField('PASS CODE', validators=[DataRequired()])
    confirm_pass_code = PasswordField('CONFIRM PASS CODE', validators=[DataRequired(), EqualTo('pass_code')])
    submit = SubmitField('ADD STUDENT')


class Courses(FlaskForm):
    className = StringField("COURSE NAME", validators=[DataRequired()])
    Teacher = SelectField("TEACHER", validators=[DataRequired()], choices=[])
    my_level = SelectField("LEVEL", validators=[DataRequired()], choices=[])
    submit = SubmitField('ADD')


class addStudent(FlaskForm):
    email = StringField('Enter Student mail', validators=[DataRequired(), Email()])
    grade = SelectField('Grade', validators=[DataRequired()],
                        choices=[('pre-primary 1'), ('pre-primary'), ('Grade 1'), ('Grade 2'), ('Grade 2'), ('Grade 3'),
                                 ('Grade 4'), ('Grade 5'),
                                 ('Grade 6'), ('Grade 7'), ('Grade 8'), ('Grade 9')])
    first_name = StringField('Students name', validators=[DataRequired(), Length(min=2, max=40)])
    second_name = StringField('Second name', validators=[DataRequired(), Length(min=2, max=40)])
    submit = SubmitField('ADD')


class CreateClass(FlaskForm):
    name = StringField('Enter Class name', validators=[DataRequired()])
    grade = SelectField('Grade', validators=[DataRequired()],
                        choices=[('pre-primary 1'), ('pre-primary'), ('Grade 1'), ('Grade 2'), ('Grade 2'), ('Grade 3'),
                                 ('Grade 4'), ('Grade 5'),
                                 ('Grade 6'), ('Grade 7'), ('Grade 8'), ('Grade 9')])
    submit = SubmitField('CREATE')


class removeStudent(FlaskForm):
    email = StringField('Enter Student mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Remove')


class Student_signup(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Second Name', validators=[DataRequired()])
    username = StringField('User Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    grade = SelectField('Grade', validators=[DataRequired()],
                        choices=[('pre-primary 1'), ('pre-primary'), ('Grade 1'), ('Grade 2'), ('Grade 2'), ('Grade 3'),
                                 ('Grade 4'), ('Grade 5'),
                                 ('Grade 6'), ('Grade 7'), ('Grade 8'), ('Grade 9')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=23)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class Student_login(FlaskForm):
    email = StringField('Enter Your Email or REGISTRATION', validators=[DataRequired()])
    password = PasswordField('Password / Passcode', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class Assignment_form(FlaskForm):
    course = SelectField("choose course", validators = [DataRequired()])
    content = TextAreaField("assignment content/instructions", validators = [DataRequired()])
    file = FileField("ATTACH FILE", validators = [FileAllowed(['docx', 'png', 'jpg', 'pdf'])])
    submit = SubmitField()

class AddLevel(FlaskForm):
    name = StringField('Class Name', validators=[DataRequired()])
    submit = SubmitField("ADD")