import pytest
from unittest.mock import MagicMock
from app import (
    listar_banco,
    listar_banco_por_id,
    adicionar_imovel,
    atualizar_imovel,
    remover_imovel,
    lista_atributo,
    lista_cidade,
)

def test_listar_banco():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(1,'giovanni',500),(2,'gabriel',1000),(3,'mini pekka',5000)]

    banco = listar_banco(mock_conn)

    mock_cursor.execute.assert_called_once_with(
        "SELECT id, proprietario, valor FROM imoveis"
    )
    assert banco == [(1,'giovanni',500),(2,'gabriel',1000),(3,'mini pekka',5000)]

def test_listar_banco_por_id():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (3,'mini pekka',5000)

    banco = listar_banco_por_id(mock_conn, 3)

    mock_cursor.execute.assert_called_once_with(
        "SELECT id, proprietario, valor FROM imoveis WHERE id = %s", (3,)
    )
    assert banco == (3,'mini pekka',5000)

def test_adicionar_imovel():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    banco = adicionar_imovel(mock_conn, 3, 'mini pekka', 5000)

    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO imoveis (id, proprietario, valor) VALUES (%s, %s, %s)",
        (3, "mini pekka", 5000)
    )
    mock_conn.commit.assert_called_once()
    assert banco == (3,'mini pekka',5000)

def test_atualizar_imovel():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    banco = atualizar_imovel(mock_conn, 3, 'mini pekka', 5000)

    mock_cursor.execute.assert_called_once_with(
        "UPDATE imoveis SET proprietario = %s, valor = %s WHERE id = %s",
        ("mini pekka", 5000, 3)
    )
    mock_conn.commit.assert_called_once()
    assert banco == (3,'mini pekka',5000)

def test_remover_imovel():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    remover_imovel(mock_conn, 3, 'mini pekka', 5000)

    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM imoveis WHERE id = %s AND proprietario = %s AND valor = %s",
        (3, "mini pekka", 5000)
    )
    mock_conn.commit.assert_called_once()

def test_lista_atributo():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    lista_atributo(mock_conn)

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis GROUP BY tipos_logradouro"
    )

def test_lista_cidade():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    lista_cidade(mock_conn)

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis GROUP BY cidade"
    )
