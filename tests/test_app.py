
import pytest
from app import create_app
from app import routes


@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SECRET_KEY="test-secret"
    )

    routes.ocorrencias.clear()

    yield app

    routes.ocorrencias.clear()


@pytest.fixture
def client(app):
    return app.test_client()


def test_pagina_inicial(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Comunidade Conectada" in response.data


def test_formulario_registro_abre(client):
    response = client.get("/registrar")

    assert response.status_code == 200
    assert b"Registrar ocorr" in response.data


def test_consulta_sem_ocorrencias(client):
    response = client.get("/consultar")

    assert response.status_code == 200
    assert "Nenhuma ocorrência registrada".encode("utf-8") in response.data


def test_cadastro_ocorrencia(client):
    response = client.post(
        "/registrar",
        data={
            "categoria": "Iluminação pública",
            "descricao": "Poste com lâmpada queimada",
            "localizacao": "Rua das Flores, Santo Antônio"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert "Iluminação pública".encode("utf-8") in response.data
    assert b"Poste com" in response.data
    assert b"Rua das Flores" in response.data
    assert b"Pendente" in response.data


def test_cadastro_invalido(client):
    response = client.post(
        "/registrar",
        data={
            "categoria": "",
            "descricao": "Descrição de teste",
            "localizacao": "Rua de teste"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert "Preencha todos os campos obrigatórios".encode(
        "utf-8") in response.data
