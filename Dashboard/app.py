from distutils.log import debug
from flask import Flask, Request, render_template, send_from_directory, Response, redirect, flash, request, url_for
from werkzeug.utils import secure_filename
import os
import sqlite3
import controller.leaf_detect
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import numpy as np


# from requests import request
from model import user

app = Flask(__name__, static_url_path='')
conn = sqlite3.connect('./agro_drone.db')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'mp4'])
UPLOAD_FOLDER = '/home/splash365/Desktop/IDP/Agro-Drone/Dashboard'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/controller/<path:path>')
def play(path):
    return send_from_directory('/controller/', path)

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('assets', path)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/field-operation')
def field_op():
    return render_template('field_op.html')
@app.route('/analysis')
def analysis():
    result = [0, 0]
    return render_template('result.html', result = result)
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
@app.route('/detect/video', methods=["POST", "GET"])
def video_detector():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            controller.leaf_detect.run_video_detector(file.filename)
            result = [0, -1]
            return render_template('result.html', result = result)
    return redirect(url_for('.analysis'))
@app.route('/detect/image', methods=["POST", "GET"])
def image_detector():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result = controller.leaf_detect.run_image_detector(file.filename)
            res = result
            summary = result.pandas().xyxy[0]
            healthy = diseased = 0
            for i in summary['name']:
                if i == 'Leaf_Healty':
                    healthy += 1
                else:
                    diseased += 1
            p_h = healthy/(healthy + diseased)
            p_h *= 100
            p_d = diseased/(healthy + diseased)
            p_d *= 100
            # %matplotlib inline
            plt.imshow(np.squeeze(result.render()))
            # plt.show()
            result = []
            result.append(p_h)
            result.append(p_d)
            res.render()
            for img in res.imgs:
                img_base64 = Image.fromarray(img)
                img_base64.save("static/assets/test.jpg", format="JPEG")
            return render_template('result.html', result = result)
    else:
        return redirect(url_for('.analysis'))
@app.route('/detect/live', methods=["POST", "GET"])
def live_detector():
    controller.leaf_detect.run_live_detector()
    return redirect(url_for('.analysis'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
