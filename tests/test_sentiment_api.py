from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_positive_text_returns_positive_sentiment() -> None:
    response = client.post(
        "/api/sentiment/analyze",
        json={
            "text": "O atendimento foi excelente e a plataforma e muito intuitiva.",
            "language": "pt",
            "include_opinion_mining": True,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "positive"
    assert any(opinion["target"] == "atendimento" for opinion in data["opinions"])


def test_negative_text_returns_negative_sentiment() -> None:
    response = client.post(
        "/api/sentiment/analyze",
        json={
            "text": "O preco esta caro e o sistema esta lento e confuso.",
            "language": "pt",
            "include_opinion_mining": True,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "negative"
    assert any(opinion["target"] == "preco" for opinion in data["opinions"])
    assert any(opinion["target"] == "produto" or opinion["target"] == "desempenho" for opinion in data["opinions"])


def test_sentence_breakdown_is_returned() -> None:
    response = client.post(
        "/api/sentiment/analyze",
        json={
            "text": "Gostei do produto. O suporte foi ruim.",
            "language": "pt",
            "include_opinion_mining": True,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["sentences"]) == 2
