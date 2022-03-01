from flask import Flask
from flask import render_template

app = Flask(__name__)

# landing page route
@app.route("/")
def land():
    return render_template('landing.html')

# teachers pannel
@app.route("/teachers")
def teachers():
    return render_template('teachers_pannel.html')


if __name__ == '__main__':
    app.run(debug=True,port=8080,use_reloader=False)