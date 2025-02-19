from flask import Flask, request, jsonify, send_from_directory

import random
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="")


def generate_password(
    length,
    include_uppercase=True,
    include_lowercase=True,
    include_numbers=True,
    include_symbols=False,
):
    """
    Generate a random password.

    Parameters:
    - length (int): Length of the password.
    - include_uppercase (bool): If True, include uppercase letters.
    - include_lowercase (bool): If True, include lowercase letters.
    - include_numbers (bool): If True, include numeric characters.
    - include_symbols (bool): If True, include special symbols.

    Returns:
    - str: The generated password, or None if no character types are selected.
    """
    characters = ""
    if include_uppercase:
        characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if include_lowercase:
        characters += "abcdefghijklmnopqrstuvwxyz"
    if include_numbers:
        characters += "0123456789"
    if include_symbols:
        characters += "!@#$%^&*()_+[]{}|;:,.<>?"

    if not characters:
        return None

    password = "".join(random.choice(characters) for _ in range(length))
    return password


@app.route("/generate", methods=["GET"])
def generate():
    """
    Endpoint to generate a random password.
    Query Parameters:
    - length: (int) Length of the password (default is 12)
    - uppercase: (str) 'true' or 'false' to include uppercase letters (default is true)
    - lowercase: (str) 'true' or 'false' to include lowercase letters (default is true)
    - numbers: (str) 'true' or 'false' to include numbers (default is true)
    - symbols: (str) 'true' or 'false' to include symbols (default is false)
    """
    try:
        length = int(request.args.get("length", 12))
    except ValueError:
        return jsonify({"error": "Invalid length provided."}), 400

    include_uppercase = request.args.get("uppercase", "true").lower() == "true"
    include_lowercase = request.args.get("lowercase", "true").lower() == "true"
    include_numbers = request.args.get("numbers", "true").lower() == "true"
    include_symbols = request.args.get("symbols", "false").lower() == "true"

    if not (
        include_uppercase or include_lowercase or include_numbers or include_symbols
    ):
        return jsonify({"error": "Please select at least one character type."}), 400

    password = generate_password(
        length, include_uppercase, include_lowercase, include_numbers, include_symbols
    )

    if password is None:
        return jsonify({"error": "Password could not be generated."}), 500

    return jsonify({"password": password})


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
