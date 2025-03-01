from flask import Flask, render_template, request, jsonify, send_file
import os
import pyaes
import secrets

app = Flask(__name__)

# Define o diretório onde os arquivos criptografados serão armazenados
OUTPUT_DIR = os.path.expanduser("~/Desktop/Encriptado")
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route("/")
def index():
    return render_template("helloWorld.html")


@app.route("/criptografar", methods=["POST"])
def criptografar():
    if "arquivo" not in request.files or request.files["arquivo"].filename == "":
        return jsonify({"erro": "Nenhum arquivo foi enviado."}), 400

    arquivo = request.files["arquivo"]
    chave = request.form.get("chave")

    # Verifica se a chave tem tamanho válido (16, 24 ou 32 bytes)
    if not chave or len(chave) not in [16, 24, 32]:
        return jsonify({"erro": "A chave deve ter 16, 24 ou 32 caracteres."}), 400

    # Lê o conteúdo do arquivo em modo binário
    file_data = arquivo.read()

    # Cria o objeto AES com o modo de operação CTR
    aes = pyaes.AESModeOfOperationCTR(chave.encode())

    # Criptografa os dados do arquivo
    encrypted_data = aes.encrypt(file_data)

    # Salva o arquivo criptografado no diretório definido
    encrypted_filename = f"{OUTPUT_DIR}/{arquivo.filename}"
    with open(encrypted_filename, "wb") as f:
        f.write(encrypted_data)

    return jsonify({"mensagem": f"Arquivo criptografado salvo em: {encrypted_filename}"})


if __name__ == "__main__":
    app.run(debug=True)
