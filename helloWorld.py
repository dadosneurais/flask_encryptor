from flask import Flask, render_template, request, jsonify
import os
import pyaes

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('helloWorld.html')

@app.route('/criptografar', methods=['POST'])
def criptografar_arquivo():
    dados = request.form
    caminho_arquivo = dados.get('caminho')  # caminho do arquivo
    chave_usuario = dados.get('chave')  # chave do input

    if not caminho_arquivo or not chave_usuario:
        return jsonify({'erro': 'Caminho do arquivo e chave são obrigatórios'}), 400

    if len(chave_usuario) not in [16, 24, 32]:
        return jsonify({'erro': 'A chave deve ter 16, 24 ou 32 bytes'}), 400

    if not os.path.exists(caminho_arquivo):
        return jsonify({'erro': 'Arquivo não encontrado'}), 404

    try:
        # converte chave para bytes
        chave_bytes = chave_usuario.encode("utf-8")

        # leitura dados do arquivo original
        with open(caminho_arquivo, 'rb') as f:
            file_data = f.read()

        if not file_data:
            return jsonify({'erro': 'O arquivo está vazio'}), 400

        # criptografia
        aes = pyaes.AESModeOfOperationCTR(chave_bytes)
        encrypted_data = aes.encrypt(file_data)

        # sobrescreve arquivo com criptografia
        with open(caminho_arquivo, 'wb') as f:
            f.write(encrypted_data)

        return jsonify({'mensagem': f'Arquivo "{caminho_arquivo}" criptografado com sucesso!'})

    except Exception as e:
        return jsonify({'erro': f'Erro ao criptografar o arquivo: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
