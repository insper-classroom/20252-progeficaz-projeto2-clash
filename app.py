import os
from flask import Flask, render_template, jsonify, request , url_for
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

def _gerar_links_imovel(imovel):
    """Gera os links HATEOAS para um objeto de imóvel."""
    imovel_id = imovel.get('id')
    if not imovel_id:
        return {} # Retorna vazio se não houver ID

    return {
        "_links": {
            "self": {
                "href": url_for('listar_banco_id_route', id=imovel_id, _external=True),
                "method": "GET"
            },
            "edit": {
                "href": url_for('atualizar_imovel_route', id=imovel_id, _external=True),
                "method": "PUT"
            },
            "delete": {
                "href": url_for('remover_imovel_route', id=imovel_id, _external=True),
                "method": "DELETE"
            }
        }
    }



def listar_banco(conn):
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                id, logradouro, tipo_logradouro, bairro, cidade, 
                cep, tipo, valor, data_aquisicao 
            FROM imoveis.imoveis
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows:
            return rows 
        else:
            return jsonify({'Erro' : 'Não encontrado'}) , 404 
    finally:
        cursor.close()
        


def listar_banco_por_id(conn, id_):
    query = """
        SELECT 
            id, logradouro, tipo_logradouro, bairro, cidade, 
            cep, tipo, valor, data_aquisicao 
        FROM imoveis.imoveis
        WHERE id = %s
    """
        # GARANTA QUE O CURSOR ESTÁ CONFIGURADO PARA RETORNAR DICIONÁRIOS
    cur = conn.cursor(dictionary=True) # <-- A SOLUÇÃO ESTÁ AQUI
    cur.execute(query, (id_,))
    row = cur.fetchone() # Agora 'row' será um dicionário: {'id': 42, 'logradouro': 'Rua...', ...}
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


# Atualize esta rota
@app.route("/imoveis", methods=["GET"])
def listar_banco_route():
    conn = get_connection()
    try:
        rows = listar_banco(conn)
        if rows:
            # Aplica o mesmo padrão HATEOAS das outras listas
            imoveis_com_links = [{**imovel, **_gerar_links_imovel(imovel)} for imovel in rows]
            
            response_data = {
                "_links": {
                    "self": { "href": url_for('listar_banco_route', _external=True) }
                },
                "count": len(imoveis_com_links),
                "_embedded": {
                    "imoveis": imoveis_com_links
                }
            }
            return jsonify(response_data), 200
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
            # JUNTA OS DADOS DO BANCO COM OS LINKS GERADOS PELA NOSSA FUNÇÃO
            response_data = {**row, **_gerar_links_imovel(row)} 
            return jsonify(response_data), 200             
        else:
            return jsonify({'erro': 'Imóvel não encontrado'}), 404
    finally:
        conn.close()


@app.route("/imoveis", methods=["POST"])
def adicionar_imovel_route():
    data = request.json
    conn = get_connection()
    try:
        # 1. Cria o imóvel no banco e obtém o objeto completo com o novo ID
        novo_imovel = adicionar_imovel(conn, data)

        # 2. Cria a representação completa do recurso, incluindo seus links HATEOAS
        response_data = {**novo_imovel, **_gerar_links_imovel(novo_imovel)}

        # 3. Gera a URL para o novo recurso, que será usada no header 'Location'
        location_url = url_for('listar_banco_id_route', id=novo_imovel['id'], _external=True)

        # 4. Retorna a resposta completa: corpo, status 201, e o header Location
        return jsonify(response_data), 201, {'Location': location_url}
    finally:
        conn.close()

@app.route("/imoveis/<int:id>", methods=["POST", "PUT"])
def atualizar_imovel_route(id):
    data = request.json
    conn = get_connection()
    try:
        # 1. Atualiza o imóvel no banco de dados
        atualizado = atualizar_imovel(conn, id, data)

        # 2. Combina os dados atualizados com seus respectivos links HATEOAS
        response_data = {**atualizado, **_gerar_links_imovel(atualizado)}

        # 3. Retorna a representação completa do recurso atualizado
        return jsonify(response_data), 200
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
        # 1. Adiciona os links HATEOAS para cada imóvel encontrado na lista
        imoveis_com_links = [{**imovel, **_gerar_links_imovel(imovel)} for imovel in rows]

        # 2. Cria uma resposta estruturada para a coleção
        response_data = {
            "_links": {
                # Link para a própria coleção que está sendo visualizada
                "self": { "href": url_for('lista_tipo', tipo=tipo, _external=True) }
            },
            "count": len(imoveis_com_links),
            # Adiciona a lista de imóveis (já com os links) em um campo separado
            "_embedded": {
                "imoveis": imoveis_com_links
            }
        }
        return jsonify(response_data), 200
    else:
        return jsonify({'erro': f'Nenhum imóvel do tipo "{tipo}" foi encontrado'}), 404


@app.route("/imoveis/cidade/<nome_cidade>", methods=["GET"])
def listar_por_cidade(nome_cidade):
    nome_cidade_tratado = nome_cidade.replace('-', ' ').lower()
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    query = "SELECT * FROM imoveis.imoveis WHERE LOWER(cidade) = %s"
    cur.execute(query, (nome_cidade_tratado,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if rows:
        # 1. Adiciona os links HATEOAS para cada imóvel retornado
        imoveis_com_links = [{**imovel, **_gerar_links_imovel(imovel)} for imovel in rows]

        # 2. Cria uma resposta estruturada para a coleção de resultados
        response_data = {
            "_links": {
                # Link para a própria consulta que está sendo feita
                "self": { "href": url_for('listar_por_cidade', nome_cidade=nome_cidade, _external=True) }
            },
            "count": len(imoveis_com_links),
            # Aninha a lista de imóveis dentro do campo _embedded
            "_embedded": {
                "imoveis": imoveis_com_links
            }
        }
        return jsonify(response_data), 200
    else:
        return jsonify({'erro': f'Nenhum imóvel encontrado para a cidade "{nome_cidade}"'}), 404
if __name__ == "__main__":
    print("Conectando-se ao DB apenas quando necessário…")
    app.run(debug=True)
