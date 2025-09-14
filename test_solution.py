import pytest
from app import app
from unittest.mock import MagicMock , patch
import requests
from app import (
    listar_banco,
    listar_banco_por_id,
    adicionar_imovel,
    atualizar_imovel,
    remover_imovel,
    lista_atributo,
    lista_cidade,
)
MOCK_IMOVEIS = [
    {
        "bairro": "Lake Danielle",
        "cep": "85184",
        "cidade": "Judymouth",
        "data_aquisicao": "2017-07-29",
        "id": 1,
        "logradouro": "Nicole Common",
        "tipo": "casa em condominio",
        "tipo_logradouro": "Travessa",
        "valor": 488424.0
    },
    {
        "bairro": "Colonton",
        "cep": "93354",
        "cidade": "North Garyville",
        "data_aquisicao": "2021-11-30",
        "id": 2,
        "logradouro": "Price Prairie",
        "tipo": "casa em condominio",
        "tipo_logradouro": "Travessa",
        "valor": 260070.0
    },
    {
        "bairro": "West Jennashire",
        "cep": "51116",
        "cidade": "Katherinefurt",
        "data_aquisicao": "2020-04-24",
        "id": 3,
        "logradouro": "Taylor Ranch",
        "tipo": "apartamento",
        "tipo_logradouro": "Avenida",
        "valor": 815970.0
    }]


@patch('app.listar_banco')
def test_valida_rota_listar_banco(mock_listar_banco):
    mock_listar_banco.return_value = MOCK_IMOVEIS
    with app.test_client() as client:
        
        response = client.get('/imoveis')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        
        json_data = response.get_json()
        assert json_data == MOCK_IMOVEIS
        mock_listar_banco.assert_called_once()
                
@patch('app.listar_banco_por_id')
def test_listar_banco_por_id(mock_listar_banco_id):
    mock_listar_banco_id.return_value = MOCK_IMOVEIS[0]  # retorna o imóvel de id 1
    with app.test_client() as client:
        response = client.get('/imoveis/1')
        assert response.status_code == 200
        assert response.get_json() == MOCK_IMOVEIS[0]
        mock_listar_banco_id.assert_called()
    
    
def test_adicionar_imovel():
    payload = {
        "bairro": "Mooca",
        "cep": "51116",
        "cidade": "São Paulo",
        "data_aquisicao": "2020-04-24",
        "logradouro": "Taylor Ranch",
        "tipo": "apartamento",
        "tipo_logradouro": "Avenida",
        "valor": 815970.0
    }

    response = requests.post("http://localhost:5000/imoveis", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert isinstance(data["id"], int)  
    assert data["bairro"] == payload["bairro"]
    assert data["cidade"] == payload["cidade"]
    assert data["valor"] == payload["valor"]
    assert data["tipo"] == payload["tipo"]









# def test_adicionar_imovel():
#     mock_conn = MagicMock()
#     mock_cursor = MagicMock()
#     mock_conn.cursor.return_value = mock_cursor

#     banco = adicionar_imovel(mock_conn, 3, 'mini pekka', 5000)

#     mock_cursor.execute.assert_called_once_with(
#         "INSERT INTO imoveis (id, proprietario, valor) VALUES (%s, %s, %s)",
#         (3, "mini pekka", 5000)
#     )
#     mock_conn.commit.assert_called_once()
#     assert banco == (3,'mini pekka',5000)










# Teste para mockar a função e testar a rota POST /imoveis/<id>
@patch('app.atualizar_imovel')
def test_rota_post_imoveis_id(mock_atualizar_imovel):
    esperado = (
        MOCK_IMOVEIS[1]['id'],
        MOCK_IMOVEIS[1]['logradouro'],
        MOCK_IMOVEIS[1]['valor']
    )
    mock_atualizar_imovel.return_value = esperado

    with app.test_client() as client:
        payload = {
            "id": MOCK_IMOVEIS[1]['id'],
            "logradouro": MOCK_IMOVEIS[1]['logradouro'],
            "valor": MOCK_IMOVEIS[1]['valor']
        }
        response = client.post(f"/imoveis/{MOCK_IMOVEIS[1]['id']}", json=payload)
        assert response.status_code == 200 or response.status_code == 201
        assert response.get_json() == list(esperado) or response.get_json() == esperado
        mock_atualizar_imovel.assert_called_once()

# def test_atualizar_imovel():
#     mock_conn = MagicMock()
#     mock_cursor = MagicMock()
#     mock_conn.cursor.return_value = mock_cursor

#     banco = atualizar_imovel(mock_conn, 3, 'mini pekka', 5000)

#     mock_cursor.execute.assert_called_once_with(
#         "UPDATE imoveis SET proprietario = %s, valor = %s WHERE id = %s",
#         ("mini pekka", 5000, 3)
#     )
#     mock_conn.commit.assert_called_once()
#     assert banco == (3,'mini pekka',5000)

# def test_remover_imovel():
#     mock_conn = MagicMock()
#     mock_cursor = MagicMock()
#     mock_conn.cursor.return_value = mock_cursor

#     remover_imovel(mock_conn, 3, 'mini pekka', 5000)

#     mock_cursor.execute.assert_called_once_with(
#         "DELETE FROM imoveis WHERE id = %s AND proprietario = %s AND valor = %s",
#         (3, "mini pekka", 5000)
#     )
#     mock_conn.commit.assert_called_once()

# def test_lista_atributo():
#     mock_conn = MagicMock()
#     mock_cursor = MagicMock()
#     mock_conn.cursor.return_value = mock_cursor

#     lista_atributo(mock_conn)

#     mock_cursor.execute.assert_called_once_with(
#         "SELECT * FROM imoveis GROUP BY tipos_logradouro"
#     )

# def test_lista_cidade():
#     mock_conn = MagicMock()
#     mock_cursor = MagicMock()
#     mock_conn.cursor.return_value = mock_cursor

#     lista_cidade(mock_conn)

#     mock_cursor.execute.assert_called_once_with(
#         "SELECT * FROM imoveis GROUP BY cidade"
#     )
