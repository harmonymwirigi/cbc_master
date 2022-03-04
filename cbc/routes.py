from cbc.model import Teacher,teacher_learner,levels,Assignment,Assignment_material,Submission_material,Submission,Strand_materials,Sub_strand,Strands,Sub_strand_materials
from cbc.form import RegistrationForm,Login
from flask import render_template, url_for
from cbc import app

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