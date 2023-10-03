import os

from flask import (
    Flask,
    render_template,
    send_from_directory,
)

from config import REPORT_DIR


app = Flask(__name__)

app.config['REPORT_FOLDER'] = str(REPORT_DIR.absolute())


@app.route('/')
def index():
    files = [f for f in os.listdir(app.config['REPORT_FOLDER']) if f.endswith('.html')]
    return render_template("index.html", files=files)


@app.route('/report/<filename>')
def serve_report(filename):
    return send_from_directory(app.config['REPORT_FOLDER'], filename)
