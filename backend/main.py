from flask import Flask, send_from_directory, request, jsonify
import os
import random

app = Flask(__name__)


def get_frontend_path(*paths):
    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "frontend", "carpooling-app", *paths
    )


# Password Generator routes
@app.route("/")
def serve_password_generator():
    """Serve the password generator frontend"""
    return send_from_directory("../frontend", "index.html")


@app.route("/generate")
def generate_password():
    """Generate password endpoint"""
    length = int(request.args.get("length", 12))
    uppercase = request.args.get("uppercase", "true").lower() == "true"
    lowercase = request.args.get("lowercase", "true").lower() == "true"
    numbers = request.args.get("numbers", "true").lower() == "true"
    symbols = request.args.get("symbols", "false").lower() == "true"

    characters = ""
    if uppercase:
        characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if lowercase:
        characters += "abcdefghijklmnopqrstuvwxyz"
    if numbers:
        characters += "0123456789"
    if symbols:
        characters += "!@#$%^&*()_+[]{}|;:,.<>?"

    if not characters:
        return jsonify({"error": "Please select at least one character type"}), 400

    password = "".join(random.choice(characters) for _ in range(length))
    return jsonify({"password": password})


# Carpooling app routes
@app.route("/carpooling/")
def serve_carpooling():
    """Serve the carpooling app frontend"""
    return send_from_directory(get_frontend_path(), "index.html")


@app.route("/carpooling/css/<path:filename>")
def serve_css(filename):
    """Serve CSS files"""
    return send_from_directory(get_frontend_path("css"), filename)


@app.route("/carpooling/js/<path:filename>")
def serve_js(filename):
    """Serve JavaScript files"""
    return send_from_directory(get_frontend_path("js"), filename)


@app.route("/carpooling/assets/<path:filename>")
def serve_assets(filename):
    """Serve assets (images, fonts, etc.)"""
    return send_from_directory(get_frontend_path("assets"), filename)


@app.route("/carpooling/<path:filename>")
def serve_carpooling_static(filename):
    """Serve other static files"""
    return send_from_directory(get_frontend_path(), filename)


# Catch-all route for SPA navigation in carpooling app
@app.route("/carpooling/", defaults={"path": ""})
@app.route("/carpooling/<path:path>")
def serve_carpooling_pages(path):
    """Handle all carpooling routes by serving index.html"""
    if "." not in path:  # Only serve index.html for routes without file extensions
        return send_from_directory(get_frontend_path(), "index.html")
    return serve_carpooling_static(path)


if __name__ == "__main__":
    app.run(debug=True)
