from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

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
    password = StringField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
