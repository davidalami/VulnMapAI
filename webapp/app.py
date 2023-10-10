import os
import json

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
    """
    Serve the main index page which displays a list of all HTML reports.

    The function scans the report folder as specified in the app's configuration
    for all HTML files and then renders them in the `index.html` template.

    Returns:
        Rendered HTML template with the list of HTML report files.
    """
    files = [f for f in os.listdir(app.config['REPORT_FOLDER']) if f.endswith('.json')]
    return render_template("index.html", files=files)


@app.route('/report/<filename>')
def serve_report(filename):
    """
    Serves a specific report file from the configured report directory.

    Returns:
        The requested report file.
    """
    kwargs = json.load(open(os.path.join(app.config['REPORT_FOLDER'], filename)))
    return render_template("report_template.html", **kwargs)
