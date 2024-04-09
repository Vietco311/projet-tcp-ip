from flask import Flask, request, jsonify
from service import Service
from main import HuffmanCode

import os

app = Flask(__name__)
huffman = HuffmanCode()

@app.route('/files', methods=['GET'])
def get_file_list():
    upload_folder = os.path.join(os.path.dirname(__file__), 'upload_folder')
    file_list = [f for f in os.listdir(upload_folder) if os.path.isfile(os.path.join(upload_folder, f))]
    return jsonify(file_list)

@app.route('/upload', methods=['POST'])
def upload_file():
    
    file = request.files['file']
    huffman.compress(file)  
    return 'File uploaded successfully'

@app.route('/download/<file_name>', methods=['GET'])
def download_file(file_name):
    file_data = huffman.decompress(file_name)
    print(file_data, "lflflflf")
    return jsonify({"file_name": file_name, "file_data": file_data})

if __name__ == '__main__':
    app.run(debug=True)
