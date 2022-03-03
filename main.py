from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] ='ThiS musT be very CONFidenTIAL'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///site.db'

# db = SQLAlchemy(app)
#
# class Teachers(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     first_name = db.Column(db.String, null = False)
#     second_name = db.Column(db.String, null = False)
#     email = db.Column(db.String, unique = True)
#     phone_number = db.Column(db.String, unique = True)
#     phone_number = db.Column(db.String, unique = True)


# landing page route
@app.route("/")
def land():
    return render_template('landing.html')

# teachers pannel
@app.route("/teachers")
def teachers():
    return render_template('teachers_pannel.html')

# signup
@app.route("/signup")
def signup():
    return render_template('teachers_pannels.html')

if __name__ == '__main__':
    app.run(debug=True,port=8080,use_reloader=False)