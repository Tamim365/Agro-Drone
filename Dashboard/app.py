from flask import Flask, Request, render_template, send_from_directory, Response, redirect
# from database import client
import sqlite3

from requests import request
from model import user

app = Flask(__name__, static_url_path='')
conn = sqlite3.connect('./agro_drone.db')


@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('assets', path)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/field-operation')
def field_op():
    return render_template('field_op.html')
@app.route('/area-status')
def area_status():
    return render_template('area_status.html')
@app.route('/area-map')
def area_map():
    return render_template('area_map.html')
@app.route('/history')
def history():
    return render_template('history.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/registerUser', methods=["POST", "GET"])
def registerUser():
    name = Request.form['name']
    # email = request.form['email'] 
    # password = request.form['password']
    print(name)
    return redirect("/")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)