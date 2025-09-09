import pytest
from app import app
from unittest.mock import MagicMock , patch
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
                
# @patch('listar_banco_por_id')
# def test_listar_banco_por_id(mock_listar_banco_id):
    



# def test_listar_banco_por_id():
#     mock_conn = MagicMock()
#     mock_cursor = MagicMock()
#     mock_conn.cursor.return_value = mock_cursor
#     mock_cursor.fetchone.return_value = (3,'mini pekka',5000)

#     banco = listar_banco_por_id(mock_conn, 3)

#     mock_cursor.execute.assert_called_once_with(
#         "SELECT id, proprietario, valor FROM imoveis WHERE id = %s", (3,)
#     )
#     assert banco == (3,'mini pekka',5000)

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
