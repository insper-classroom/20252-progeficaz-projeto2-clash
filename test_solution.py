import pytest
from app import app
from unittest.mock import MagicMock, patch
import requests
from app import (
    listar_banco,
    listar_banco_por_id,
    adicionar_imovel,
    atualizar_imovel,
    remover_imovel,
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
        imoveis = json_data['_embedded']['imoveis']
        for i, imovel in enumerate(imoveis):
            for campo in MOCK_IMOVEIS[i]:
                assert imovel[campo] == MOCK_IMOVEIS[i][campo]
        mock_listar_banco.assert_called_once()


@patch('app.listar_banco_por_id')
def test_listar_banco_por_id(mock_listar_banco_id):
    mock_listar_banco_id.return_value = MOCK_IMOVEIS[0]
    with app.test_client() as client:
        response = client.get('/imoveis/1')
        assert response.status_code == 200
        json_data = response.get_json()
        for campo in MOCK_IMOVEIS[0]:
            assert json_data[campo] == MOCK_IMOVEIS[0][campo]
        mock_listar_banco_id.assert_called()


@patch('app.adicionar_imovel')
def test_adicionar_imovel(mock_adicionar_imovel):
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

    mock_adicionar_imovel.return_value = {**payload, "id": 1}

    with app.test_client() as client:
        response = client.post("/imoveis", json=payload)

        assert response.status_code == 201
        assert response.content_type == "application/json"

        data = response.get_json()
        assert "id" in data
        assert data["id"] == 1
        assert data["bairro"] == payload["bairro"]
        assert data["cidade"] == payload["cidade"]
        assert data["valor"] == payload["valor"]
        assert data["tipo"] == payload["tipo"]

        mock_adicionar_imovel.assert_called_once()


@patch('app.atualizar_imovel')
def test_atualizar_imovel(mock_atualizar_imovel):
    payload = {
        "logradouro": "Rua da Mooca",
        "valor": 777.0
    }
    esperado = {"id": 1, "logradouro": payload["logradouro"], "valor": payload["valor"]}
    mock_atualizar_imovel.return_value = esperado

    with app.test_client() as client:
        response = client.post("/imoveis/1", json=payload)

        assert response.status_code == 200
        data = response.get_json()
        assert data["id"] == esperado["id"]
        assert data["logradouro"] == esperado["logradouro"]
        assert data["valor"] == esperado["valor"]

        mock_atualizar_imovel.assert_called_once()


@patch('app.remover_imovel')
def test_remover_imovel(mock_remover_imovel):
    mock_remover_imovel.return_value = None

    with app.test_client() as client:
        response = client.delete("/imoveis/1")

        assert response.status_code == 204
        assert response.data == b''

        mock_remover_imovel.assert_called_once()


@patch('app.listar_por_cidade')
def test_rota_listar_por_cidade(mock_listar_cidade):
    mock_listar_cidade.return_value = [MOCK_IMOVEIS[0]]
    with app.test_client() as client:
        response = client.get('/imoveis/cidade/Judymouth')
        json_data = response.get_json()
        assert response.status_code == 200
        imoveis = json_data['_embedded']['imoveis']
        assert imoveis[0]['cidade'] == 'Judymouth'


@patch('app.lista_tipo')
def test_rota_listar_por_tipo(mock_listar_cidade):
    mock_listar_cidade.return_value = [MOCK_IMOVEIS[2]]
    with app.test_client() as client:
        response = client.get('/imoveis/tipo/apartamento')
        assert response.status_code == 200
        json_data = response.get_json()
        imoveis = json_data['_embedded']['imoveis']
        for imovel in imoveis:
            assert imovel['tipo'] == 'apartamento'
