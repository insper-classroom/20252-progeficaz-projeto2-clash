import os
from flask import Flask, render_template, jsonify , redirect , request
import mysql.connector
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),   
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_ca=os.getenv("DB_SSL_CA"),   # caminho válido
        ssl_verify_cert=True,
        connection_timeout=15,
        read_timeout=60,
        write_timeout=60,
    )

def listar_banco(conn):
    """
    Busca todos os imóveis no banco de dados e retorna uma LISTA DE DICIONÁRIOS.
    """
    cursor = conn.cursor(dictionary = True) 
    query = """
        SELECT 
            id, logradouro, tipo_logradouro, bairro, cidade, 
            cep, tipo, valor, data_aquisicao 
        FROM imoveis.imoveis
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows

def listar_banco_por_id(conn, id_):
    '''
    Busca o imóvel com o id condizente 
    '''
    
    query = """
        SELECT 
            id, logradouro, tipo_logradouro, bairro, cidade, 
            cep, tipo, valor, data_aquisicao 
        FROM imoveis.imoveis
        WHERE id = %s
    """
    cur = conn.cursor(dictionary=True)
    cur.execute(query, (id_,))
    row = cur.fetchone()
    cur.close()
    return row


def atualizar_imovel(conn, id_, proprietario, valor):
    cur = conn.cursor()
    cur.execute(
        "UPDATE imoveis.imoveis SET proprietario = %s, valor = %s WHERE id = %s",
        (proprietario, valor, id_),
    )
    conn.commit()
    cur.close()
    return (id_, proprietario, valor)

def remover_imovel(conn, id_, proprietario, valor):
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM imoveis.imoveis WHERE id = %s AND proprietario = %s AND valor = %s",
        (id_, proprietario, valor),
    )
    conn.commit()
    cur.close()

def lista_atributo(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM imoveis.imoveis GROUP BY tipos_logradouro")
    rows = cur.fetchall()
    cur.close()
    return rows

def lista_cidade(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM imoveis.imoveis GROUP BY cidade")
    rows = cur.fetchall()
    cur.close()
    return rows

def adicionar_imovel(conn, data):
    cur = conn.cursor()
    query = """
        INSERT INTO imoveis.imoveis 
            (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cur.execute(
        query,
        (
            data["logradouro"],
            data["tipo_logradouro"],
            data["bairro"],
            data["cidade"],
            data["cep"],
            data["tipo"],
            data["valor"],
            data["data_aquisicao"],
        ),
    )
    conn.commit()
    new_id = cur.lastrowid
    cur.close()
    return {**data, "id": new_id}

def atualizar_imovel(conn, id_, data):
    
    cur = conn.cursor()
    query = """
        UPDATE imoveis.imoveis
        SET logradouro = %s,
            tipo_logradouro = %s,
            bairro = %s,
            cidade = %s,
            cep = %s,
            tipo = %s,
            valor = %s,
            data_aquisicao = %s
        WHERE id = %s
    """
    cur.execute(
        query,
        (
            data["logradouro"],
            data["tipo_logradouro"],
            data["bairro"],
            data["cidade"],
            data["cep"],
            data["tipo"],
            data["valor"],
            data["data_aquisicao"],
            id_,
        ),
    )
    conn.commit()
    cur.close()
    return {**data, "id": id_}




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/imoveis", methods=["GET"])
def listar_banco_route():
    conn = get_connection()
    try:
        rows = listar_banco(conn)
        return jsonify(rows)
    finally:
        conn.close()
        
        
@app.route("/imoveis/<int:id>" , methods =["GET"])
def listar_banco_id_route(id):
    conn = get_connection()
    try:
        rows = listar_banco_por_id(conn , id)
        return jsonify(rows)
    finally:
        conn.close()
        
@app.route("/imoveis", methods=["POST"])
def adicionar_imovel_route():
    data = request.json
    conn = get_connection()
    try:
        novo_imovel = adicionar_imovel(conn, data)
        return jsonify(novo_imovel), 201
    finally:
        conn.close()

@app.route("/imoveis/<int:id>", methods=["POST", "PUT"])
def atualizar_imovel_route(id):
    data = request.json
    conn = get_connection()
    try:
        atualizado = atualizar_imovel(conn, id, data)
        return jsonify(atualizado), 200
    finally:
        conn.close()

       
    

if __name__ == "__main__":
    print("Conectando-se ao DB apenas quando necessário…")
    app.run(debug=True)
