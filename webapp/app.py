import os
import json
import openai
from dotenv import load_dotenv

from flask import (
    Flask,
    render_template,
    send_from_directory,
    request, jsonify
)

from config import REPORT_DIR


app = Flask(__name__)

app.config['REPORT_FOLDER'] = str(REPORT_DIR.absolute())

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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

@app.route('/ask-chatgpt', methods=['POST'])
def ask_chatgpt():
    """
    Handle POST requests to obtain responses from ChatGPT.

    This function is responsible for processing POST requests containing user queries
    and sending these queries to the ChatGPT API for responses. It then returns the
    generated response in a JSON format.

    Returns:
        JSON response containing the ChatGPT response to the user's query.
    """
    # Extract the user's query from the POST request data
    user_query = request.form['query']

    # Check if the 'query' parameter is provided in the request
    if not user_query:
        return jsonify({"error": "Please provide a 'query' parameter in the POST request."}), 400

    try:
        # Make a request to the ChatGPT API
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can choose a different engine if needed
            prompt=user_query,
            max_tokens=50,  # Adjust the max tokens as per your requirements
            n = 1  # Number of responses to generate
        )

        # Extract the response text from the API response
        chatgpt_response = response.choices[0].text

        # Return the ChatGPT response as JSON
        return jsonify({"response": chatgpt_response})

    except Exception as e:
        # Handle any exceptions that may occur during the API request
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run()