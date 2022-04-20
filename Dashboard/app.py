from flask import Flask, render_template, send_from_directory, Response

app = Flask(__name__, static_url_path='')

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('assets', path)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)