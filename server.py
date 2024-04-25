from flask import Flask, request, jsonify
from main import HuffmanCode
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

huffman = HuffmanCode()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({"message": "Missing username, password, or email"}), 400

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"message": "Username already exists"}), 409

    new_user = User(username=username, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or user.password != password:
        return jsonify({"message": "Invalid username or password"}), 401

    return jsonify({"message": "Login successful", "email": user.email}), 200


@app.route('/files', methods=['GET'])
def get_file_list():
    upload_folder = os.path.join(os.path.dirname(__file__), 'upload_folder')
    file_list = [f for f in os.listdir(upload_folder) if os.path.isfile(os.path.join(upload_folder, f))]
    return jsonify(file_list)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file_size = os.stat(file.filename).st_size
    print(file_size)
    huffman.compress(file)  
    return 'File uploaded successfully'

@app.route('/download/<file_name>', methods=['GET'])
def download_file(file_name):
    file_size = os.stat(f"upload_folder/{file_name}.bin").st_size
    print(file_size)
    file_data = huffman.decompress(file_name)
    return jsonify({"file_name": file_name, "file_data": file_data})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
