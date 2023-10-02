import os

from flask import (
    Flask,
    send_from_directory
)


app = Flask(__name__)
REPORT_FOLDER = './report'
app.config['REPORT_FOLDER'] = REPORT_FOLDER


@app.route('/')
def index():
    files = [f for f in os.listdir(REPORT_FOLDER) if f.endswith('.html')]
    links = [f"<a href='/report/{f}'>{f}</a>" for f in files]
    return '<br>'.join(links)


@app.route('/report/<filename>')
def serve_report(filename):
    return send_from_directory(app.config['REPORT_FOLDER'], filename)
