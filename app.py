from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def is_password_strong(password, username, common_words):
    # Check for minimum length
    if len(password) < 17:
        return False

    if not any(c.isupper() for c in password):
        return False

    if not any(c.islower() for c in password):
        return False

    if not any(c.isdigit() for c in password):
        return False

    if not re.search(r'[!@#$%^&*()_+{}[\]:;<>,.?~\\-]', password):
        return False

    # Check for common words
    for word in common_words:
        if word in password.lower():
            return False

    # Check for password repetition (consecutive characters)
    if re.search(r'(.)\1{2,}', password):
        return False

    # Check for years in the range 1900-2099 (commonly associated with birthdays)
    if re.search(r'\b(?:19|20)\d{2}\b', password):
        return False

    # Check for the username in the password
    if username and username.lower() in password.lower():
        return False

    return True

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.get_json()
    password = data.get('password')
    username = data.get('username')  # Add this field in your input
    common_words = ["password", "123456", "qwerty", "admin"]

    is_strong = is_password_strong(password, username, common_words)

    return jsonify({'isStrong': is_strong})

if __name__ == '__main__':
    app.run()
