import os

from flask import (
    Flask,
    render_template_string,
    send_from_directory,
)

from config import REPORT_DIR


app = Flask(__name__)

app.config['REPORT_FOLDER'] = str(REPORT_DIR.absolute())


@app.route('/')
def index():
    files = [f for f in os.listdir(app.config['REPORT_FOLDER']) if f.endswith('.html')]

    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Report Index</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
    </head>
    <body>
        <div class="container">
            <h4 class="center-align">Report Index</h4>
            <ul class="collection">
                {% for file in files %}
                    <li class="collection-item"><a href="/report/{{ file }}">{{ file }}</a></li>
                {% endfor %}
            </ul>
        </div>

        <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
    </body>
    </html>
    '''

    return render_template_string(html, files=files)



@app.route('/report/<filename>')
def serve_report(filename):
    return send_from_directory(app.config['REPORT_FOLDER'], filename)
