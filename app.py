
from flask import Flask, render_template, request, send_file
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import io
import base64

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000,
    )

    return base64.urlsafe_b64encode(kdf.derive(password.encode())

    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process_file():
    uploaded_file = request.files.get("file")
    password = request.form.get("password", "")
    action = request.form.get("action", "")

    if not uploaded_file or uploaded_file.filename == "":
        return "Please select a file.", 400

    if len(password) < 8:
        return "Password must be at least 8 characters long.", 400

    if action not in ("encrypt", "decrypt"):
        return "Invalid action.", 400

    file_data = uploaded_file.read()
    original_name = uploaded_file.filename

    try:
        if action == "encrypt":
            salt = os.urandom(16)
            key = generate_key(password, salt)
            encrypted_data = Fernet(key).encrypt(file_data)
            output_data = salt + encrypted_data
            output_name = original_name + ".enc"

        else:
            if len(file_data) < 17:
                return "Invalid encrypted file.", 400

            salt = file_data[:16]
            encrypted_data = file_data[16:]
            key = generate_key(password, salt)
            output_data = Fernet(key).decrypt(encrypted_data)

            if original_name.endswith(".enc"):
                output_name = original_name[:-4]
            else:
                output_name = "decrypted_" + original_name

    except InvalidToken:
        return "Wrong password or invalid encrypted file.", 400

    return send_file(
        io.BytesIO(output_data),
        as_attachment=True,
        download_name=output_name,
    )


if __name__ == "__main__":
    app.run(debug=True)
