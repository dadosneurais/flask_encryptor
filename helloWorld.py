from flask import Flask, render_template, request, send_file, jsonify
import os
import pyaes
from werkzeug.utils import secure_filename

app = Flask(__name__)

desktop_path = os.path.expanduser("~/Desktop/Encriptado")
os.makedirs(desktop_path, exist_ok=True)

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
        nome_arquivo = secure_filename(arquivo.filename)
        caminho_arquivo = os.path.join(desktop_path, nome_arquivo)

        arquivo.save(caminho_arquivo)

        with open(caminho_arquivo, 'rb') as f:
            file_data = f.read()

        if not file_data:
            return jsonify({'erro': 'O arquivo está vazio'}), 400

        chave_bytes = chave_usuario.encode("utf-8")

        aes = pyaes.AESModeOfOperationCTR(chave_bytes)
        encrypted_data = aes.encrypt(file_data)

        caminho_encriptado = os.path.join(desktop_path, f"{nome_arquivo}")
        with open(caminho_encriptado, 'wb') as f:
            f.write(encrypted_data)

        return send_file(caminho_encriptado, as_attachment=True)

    except Exception as e:
        return jsonify({'erro': f'Erro ao criptografar o arquivo: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
