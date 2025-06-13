import os
import sqlite3
import pickle
import subprocess
from flask import Flask, request, make_response

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

# Vulnérabilité 2 : Commande système
@app.route('/ping')
def ping():
    host = request.args.get('host')
    os.system(f"ping -c 1 {host}")
    return "Ping sent"

# Vulnérabilité 3 : Téléversement de fichiers non sécurisé
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(f"/tmp/{file.filename}")
    return "File uploaded"

# Vulnérabilité 4 : Désérialisation non sécurisée
@app.route('/deserialize', methods=['POST'])
def deserialize():
    data = request.data
    obj = pickle.loads(data)  # ⚠️ Très dangereux si data provient d'un client
    return f"Deserialized: {obj}"

# Vulnérabilité 5 : Cross-Site Scripting (XSS)
@app.route('/xss')
def xss():
    name = request.args.get('name', '')
    return f"<html><body>Hello {name}!</body></html>"  # Pas d'échappement du contenu

# Vulnérabilité 6 : Réponse contenant des cookies sensibles sans flag
@app.route('/set_cookie')
def set_cookie():
    resp = make_response("Cookie set")
    resp.set_cookie("session_id", "insecure-session-id")  # Manque HttpOnly, Secure
    return resp

# Vulnérabilité 7 : Exécution de commande avec subprocess
@app.route('/run')
def run():
    cmd = request.args.get('cmd')
    result = subprocess.check_output(cmd, shell=True)  # ⚠️ RCE potentiel
    return result

# Vulnérabilité 8 : Répertoire parent accessible (path traversal)
@app.route('/read_file')
def read_file():
    filename = request.args.get('file')
    with open(f"./files/{filename}", "r") as f:
        return f.read()
