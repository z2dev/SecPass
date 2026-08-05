"""
AI Assistance Notice

Artificial intelligence (ChatGPT) was used as a supporting tool during the
development of this project. The project idea, application logic, and overall
design were created by the author.
"""

from flask import Flask, render_template, request, jsonify
from utils.analyzer import analyze_password
from utils.generator import generate_password

app = Flask(__name__)

@app.route("/")
def index():

    return render_template("index.html")


# ==========================================================
# Analyze Password
# ==========================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    if not data:

        return jsonify({

            "error": "No data received."

        }), 400

    password = data.get("password", "").strip()

    if password == "":

        return jsonify({

            "error": "Password cannot be empty."

        }), 400

    result = analyze_password(password)

    return jsonify(result)


# ==========================================================
# Password Generator
# ==========================================================

@app.route("/generate", methods=["POST"])
def generate():

    password = generate_password()

    return jsonify({

        "password": password

    })


# ==========================================================
# API Status
# ==========================================================

@app.route("/api/status")
def api_status():

    return jsonify({

        "status": "online",

        "version": "1.0",

        "service": "SecPass Password Analyzer"

    })


# ==========================================================
# Error Handlers
# ==========================================================


@app.errorhandler(404)
def not_found(error):
    return render_template(
        "error.html",
        code=404,
        title="Page Not Found",
        message="Sorry, the page you're looking for doesn't exist."
    ), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return render_template(
        "error.html",
        code=405,
        title="Method Not Allowed",
        message="The requested action is not allowed on this page."
    ), 405

@app.errorhandler(500)
def internal_error(error):
    return render_template(
        "error.html",
        code=500,
        title="Internal Server Error",
        message="Something went wrong while processing your request."
    ), 500


# ==========================================================
# Run Application
# ==========================================================

if __name__ == "__main__":

    app.config["JSON_SORT_KEYS"] = False

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )

