import pytest
from unittest.mock import MagicMock

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

    banco = listar_banco_por_id(mock_conn,3)

    mock_cursor.execute.assert_called_once_with(
        "SELECT id, proprietario, valor FROM imoveis WHERE id = ?", (3,)
    )

    assert banco == (3,'mini pekka',5000)

def test_adicionar_imovel():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    banco = adicionar_imovel(mock_conn,3,'mini pekka',5000)

    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO imoveis (id, proprietario, valor) VALUES (?, ?, ?)",
        (3, "mini pekka", 5000)
    )
    mock_conn.commit.assert_called_once()

    assert banco == (3,'mini pekka',5000)