from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def land():
    return render_template('landing.html')


if __name__ == '__main__':
    app.run(debug=True,port=8080,use_reloader=False)