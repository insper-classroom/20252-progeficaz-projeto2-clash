import pytest
from app import app
from unittest.mock import MagicMock , patch

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
    mock_listar_banco_id.return_value = MOCK_IMOVEIS[0]  
    with app.test_client() as client:
        response = client.get('/imoveis/1')
        assert response.status_code == 200
        assert response.get_json() == MOCK_IMOVEIS[0]
        mock_listar_banco_id.assert_called()
        
@patch('app.listar_por_cidade')
def test_rota_listar_por_cidade(mock_listar_cidade):
    mock_listar_cidade.return_value = [MOCK_IMOVEIS[0]]
    with app.test_client() as client:
        response = client.get('/imoveis/cidade/Judymouth')
        json = response.get_json()
        assert response.status_code == 200
        assert json[0][4] == 'Judymouth'
        
        

@patch('app.listar_tipo')
def test_rota_listar_por_tipo(mock_listar_cidade):
    mock_listar_cidade.return_value = [MOCK_IMOVEIS[2]]
    with app.test_client() as client:
        response = client.get('/imoveis/tipo/apartamento')
        assert response.status_code == 200
        for imovel in response.get_json():
            assert imovel[0][6] == 'apartamento'
        mock_listar_cidade.assert_called_once()
