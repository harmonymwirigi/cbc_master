from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from cbc.model import Teacher,teacher_learner,Learner,levels,Assignment,Assignment_material,Submission_material,Submission,Strand_materials,Sub_strand,Strands,Sub_strand_materials

levels = ['pre-primary 1', 'pre-primary', 'Grade 1', 'Grade 2', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5',
          'Grade 6', 'Grade 7', 'Grade 8', 'Grade 9']
def lev():
    for i in range(len(levels)):
        if i < len(levels)-1:
            return print("('", levels[i], "'),")

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Second Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    gender = SelectField('Gender', validators=[DataRequired()], choices=[('Male'),('Female'),('others')])
    user_name = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min = 2, max = 23)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class Login(FlaskForm):
    email = StringField('Enter Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class addStudent(FlaskForm):
    email =StringField('Enter Student mail', validators=[DataRequired(), Email()])
    grade = SelectField('Grade', validators=[DataRequired()], choices=[('pre-primary 1'),('pre-primary'), ('Grade 1'), ('Grade 2'), ('Grade 2'), ('Grade 3'), ('Grade 4'),('Grade 5'),
                                                                       ('Grade 6'), ('Grade 7'), ('Grade 8'), ('Grade 9')])
    first_name = StringField('Students name', validators =[DataRequired()])
    second_name = StringField('Second name', validators =[DataRequired()])
    submit = SubmitField('ADD')

    def validate_email(self, email):
        user = Learner.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The student exist')

class removeStudent(FlaskForm):
    email = StringField('Enter Student mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Remove')

    def validate_email(self, email):
        user = Learner.query.filter_by(email=email.data).first()
        if user == 0:
            raise ValidationError('The the student does not exist')