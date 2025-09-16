import os
from flask import Flask, render_template, jsonify, request
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_ca=os.getenv("DB_SSL_CA"),  # caminho válido
        ssl_verify_cert=True,
        connection_timeout=15,
        read_timeout=60,
        write_timeout=60,
    )


def listar_banco(conn):
    cursor = conn.cursor(dictionary=True)
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


def remover_imovel(conn, id_):
    cur = conn.cursor()
    cur.execute("DELETE FROM imoveis.imoveis WHERE id = %s", (id_,))
    conn.commit()
    cur.close()


@app.route("/imoveis", methods=["GET"])
def listar_banco_route():
    conn = get_connection()
    try:
        rows = listar_banco(conn)
        if rows:
            return jsonify(rows), 200
        else:
            return jsonify({'erro': 'Nenhum imóvel encontrado'}), 404
    finally:
        conn.close()


@app.route("/imoveis/<int:id>", methods=["GET"])
def listar_banco_id_route(id):
    conn = get_connection()
    try:
        row = listar_banco_por_id(conn, id)
        if row:
            return jsonify(row), 200
        else:
            return jsonify({'erro': 'Imóvel não encontrado'}), 404
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


@app.route("/imoveis/<int:id>", methods=["DELETE"])
def remover_imovel_route(id):
    conn = get_connection()
    try:
        remover_imovel(conn, id)
        return "", 204
    finally:
        conn.close()


@app.route("/imoveis/tipo/<tipo>")
def lista_tipo(tipo):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM imoveis.imoveis WHERE tipo = %s", (tipo,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if rows:
        return jsonify(rows), 200
    else:
        return jsonify({'erro': 'Imóvel não encontrado'}), 404


@app.route("/imoveis/cidade/<nome_cidade>", methods=["GET"])
def listar_por_cidade(nome_cidade):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    query = "SELECT * FROM imoveis.imoveis WHERE cidade = %s"
    cur.execute(query, (nome_cidade,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if rows:
        return jsonify(rows), 200
    else:
        return jsonify({'erro': 'Imóvel não encontrado'}), 404


if __name__ == "__main__":
    print("Conectando-se ao DB apenas quando necessário…")
    app.run(debug=True)
