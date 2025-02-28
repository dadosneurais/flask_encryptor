import os
import pyaes
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "criptografias")

os.makedirs(DESKTOP_PATH, exist_ok=True)
app.config["UPLOAD_FOLDER"] = DESKTOP_PATH

@app.route('/')
def index():
    return render_template('helloWorld.html')

@app.route('/criptografar', methods=['POST'])
def criptografar_arquivo():
    if "arquivo" not in request.files:
        return jsonify({'erro': 'Nenhum arquivo enviado'}), 400

    arquivo = request.files["arquivo"]
    chave_usuario = request.form.get("chave")

    if not chave_usuario or len(chave_usuario) not in [16, 24, 32]:
        return jsonify({'erro': 'A chave precisa ter 16, 24 ou 32 bytes'}), 400

    if arquivo.filename == '':
        return jsonify({'erro': 'Nenhum arquivo selecionado'}), 400

    try:
        # salva o arquivo no Desktop
        caminho_arquivo = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(arquivo.filename))
        arquivo.save(caminho_arquivo)

        with open(caminho_arquivo, 'rb') as f:
            file_data = f.read()

        if not file_data:
            return jsonify({'erro': 'O arquivo está vazio'}), 400

        # converte para bytes
        chave_bytes = chave_usuario.encode("utf-8")

        # Criptografia
        aes = pyaes.AESModeOfOperationCTR(chave_bytes)
        encrypted_data = aes.encrypt(file_data)

        with open(caminho_arquivo, 'wb') as f:
            f.write(encrypted_data)

        return jsonify({'mensagem': f'Arquivo "{arquivo.filename}" criptografado com sucesso e salvo no Desktop!'}), 200

    except Exception as e:
        return jsonify({'erro': f'Erro ao criptografar o arquivo: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
