from flask import Flask, render_template, send_from_directory, Response
from database import client

app = Flask(__name__, static_url_path='')

print(client)

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
    return render_template('history.html', client=client)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)