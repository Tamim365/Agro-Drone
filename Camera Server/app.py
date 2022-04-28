from flask import Flask, Response
from cameras import usb_cam


app = Flask(__name__)

@app.route('/cam')
def cam():
    return Response(usb_cam(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host='192.168.1.155',port=5000,debug=True,threaded=True)


