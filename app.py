import os
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# Vulnérabilité 1 : Injection SQL
@app.route('/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    
    if cursor.fetchone():
        return "Logged in!"
    else:
        return "Access denied"

# Vulnérabilité 2 : Commande système non sécurisée
@app.route('/ping')
def ping():
    host = request.args.get('host')
    os.system(f"ping -c 1 {host}")
    return "Ping sent"

# Vulnérabilité 3 : Téléversement non sécurisé de fichiers
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(f"/tmp/{file.filename}")
    return "File uploaded"
