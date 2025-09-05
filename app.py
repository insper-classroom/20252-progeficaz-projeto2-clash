import os
from flask import Flask, render_template, jsonify
import mysql.connector

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "imoveis-gabrielchavesaguiar-6e57.d.aivencloud.com"),
        port=int(os.getenv("DB_PORT", "3306")),   
        user=os.getenv("DB_USER", "avnadmin"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "defaultdb"),
        ssl_ca=os.getenv("DB_SSL_CA"),            
        ssl_verify_cert=True,
        connection_timeout=15,
        read_timeout=60,
        write_timeout=60,
    )

def listar_banco(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, proprietario, valor FROM imoveis")
    rows = cur.fetchall()
    cur.close()
    return rows

def listar_banco_por_id(conn, id_):
    cur = conn.cursor()
    cur.execute("SELECT id, proprietario, valor FROM imoveis WHERE id = %s", (id_,))
    row = cur.fetchone()
    cur.close()
    return row

def adicionar_imovel(conn, id_, proprietario, valor):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO imoveis (id, proprietario, valor) VALUES (%s, %s, %s)",
        (id_, proprietario, valor),
    )
    conn.commit()
    cur.close()
    return (id_, proprietario, valor)

def atualizar_imovel(conn, id_, proprietario, valor):
    cur = conn.cursor()
    cur.execute(
        "UPDATE imoveis SET proprietario = %s, valor = %s WHERE id = %s",
        (proprietario, valor, id_),
    )
    conn.commit()
    cur.close()
    return (id_, proprietario, valor)

def remover_imovel(conn, id_, proprietario, valor):
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM imoveis WHERE id = %s AND proprietario = %s AND valor = %s",
        (id_, proprietario, valor),
    )
    conn.commit()
    cur.close()

def lista_atributo(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM imoveis GROUP BY tipos_logradouro")
    rows = cur.fetchall()
    cur.close()
    return rows

def lista_cidade(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM imoveis GROUP BY cidade")
    rows = cur.fetchall()
    cur.close()
    return rows

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/listar_banco", methods=["GET"])
def listar_banco_route():
    conn = get_connection()
    try:
        rows = listar_banco(conn)
        return jsonify(rows)
    finally:
        conn.close()

if __name__ == "__main__":
    print("Conectando-se ao DB apenas quando necessário…")
    app.run(debug=True)

# db uri mysql://avnadmin:AVNS_u_gBBUfm-q-BTx9ochl@imoveis-gabrielchavesaguiar-6e57.d.aivencloud.com:16428/defaultdb?ssl-mode=REQUIRED