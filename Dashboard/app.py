from flask import Flask, Request, render_template, send_from_directory, Response, redirect, flash, request
from werkzeug.utils import secure_filename
import os
import sqlite3
#import controller.leaf_detect
#from matplotlib import pyplot as plt
import numpy as np

# from requests import request
from model import user

app = Flask(__name__, static_url_path='')
conn = sqlite3.connect('./agro_drone.db')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = '/home/splash365/Desktop/IDP/Agro-Drone/Dashboard'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
@app.route('/get_status', methods=["POST", "GET"])    
def get_status():
    if request.method=='POST':
        try:
            name =request.form['name']
            id =request.form['id']
            totalarea =request.form['totalarea']
            scantime =request.form['scantime']
            officer =request.form['officer']
            status =request.form['status']
            
            conn = sqlite3.connect("./agro_drone.db")
            cur = conn.cursor()
            cur.execute("INSERT into agri_status(Area_name,Area_ID,Total_area,Scan_time,Officer,Status)values(?,?,?,?,?,?)",(name,id,totalarea,scantime,officer,status))
            conn.commit()
            flash('Record added Successfully',"success")
              
        except:
            flash("Error in inserting","danger")
        finally:
            return redirect("/get_status")
                   
    return render_template('area_status.html')

def index_show():   
    conn = sqlite3.connect('./agro_drone.db')
    conn.row_factory = sqlite3.Row
    return conn
 
@app.route('/show_status')
def show_status():
    conn = index_show()
    rows = conn.execute('SELECT * FROM agri_status').fetchall()
    return render_template("area_status.html", rows=rows)
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
# @app.route('/detect/video', methods=["POST", "GET"])
# def video_detector():
#     controller.leaf_detect.run_video_detector()
#     return redirect("/")
# @app.route('/detect/image', methods=["POST", "GET"])
# def image_detector():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             result = controller.leaf_detect.run_image_detector(file.filename)
#             summary = result.pandas().xyxy[0]
#             healthy = diseased = 0
#             for i in summary['name']:
#                 if i == 'Leaf_Healty':
#                     healthy += 1
#                 else:
#                     diseased += 1
#             p_h = healthy/(healthy + diseased)
#             p_h *= 100
#             p_d = diseased/(healthy + diseased)
#             p_d *= 100
#             # %matplotlib inline
#             plt.imshow(np.squeeze(result.render()))
#             # plt.show()
#             result = []
#             result.append(p_h)
#             result.append(p_d)
#             return render_template('result.html', result = result, plt = plt)




if __name__ == "__main__":
     app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
