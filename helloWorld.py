from flask import Flask, render_template, request, send_file
import os
import pyaes

app = Flask(__name__)

SERVER_DIR = os.path.abspath('')
os.makedirs(SERVER_DIR, exist_ok=True)

ENCRYPTED_FILE = os.path.join(SERVER_DIR, "encrypted")
KEYS_FILE = os.path.join(SERVER_DIR, "keys.txt")


@app.route("/")
def index():
    return render_template("helloWorld.html")


@app.route("/criptografar", methods=["POST"])
def criptografar():
    if "arquivo" not in request.files or request.files["arquivo"].filename == "":
        return "Nenhum arquivo foi enviado.", 400

    arquivo = request.files["arquivo"]
    chave = request.form.get("chave")

    if not chave or len(chave) not in [16, 24, 32]:
        return "A chave deve ter 16, 24 ou 32 caracteres.", 400

    file_data = arquivo.read()

    aes = pyaes.AESModeOfOperationCTR(chave.encode())

    encrypted_data = aes.encrypt(file_data)

    with open(ENCRYPTED_FILE, "wb") as f:
        f.write(encrypted_data)

    with open(KEYS_FILE, "a") as f:
        f.write(chave + '\n')

    return send_file(ENCRYPTED_FILE, as_attachment=True, download_name="encrypted")

@app.route("/keys.txt")
def download_keys():
    if not os.path.exists(KEYS_FILE):
        return "Nenhuma chave encontrada.", 404
    return send_file(KEYS_FILE, as_attachment=True, download_name="keys.txt")

@app.route("/encrypted")
def download_encrypted():
    if not os.path.exists(ENCRYPTED_FILE):
        return "Nenhuma chave encontrada.", 404
    return send_file(ENCRYPTED_FILE, as_attachment=True, download_name="encrypted")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
