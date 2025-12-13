# tests/test_backend_api.py
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from API_IA.sentiment_api import app

client = TestClient(app)


def test_analyse_sentiment():
    quote = {"text": "congratulations"}
    response = client.post("/analyse_sentiment", json=quote)

    # on verifie que la connexion s'etablit correctement
    assert response.status_code == 200

    # on verifie que la réponse est bien un json
    assert response.headers["content-type"].startswith("application/json")

    data = response.json()

    # on verifie que data est bien un dictionnaire 
    assert isinstance(data, dict)

    # on verifie que les 4 clés du json retourné par sentiment_api existent
    assert "neg" in data
    assert "neu" in data
    assert "pos" in data
    assert "compound" in data

    # duplicata pour mes connaissances perso
    for key in ("neg", "neu", "pos", "compound"):
        assert key in data

    # on verifie le type des valeurs correspondantes a chaques clés ici des float
    assert isinstance(data["neg"], float)
    assert isinstance(data["neu"], float)
    assert isinstance(data["pos"], float)
    assert isinstance(data["compound"], float)

    # on verifie les valeurs 
    # on les connait pour "congratulations"
    # [{"neg":0},{"neu":0},{"pos":1},{"compound":0.5994}]
    assert data["neg"] == 0
    assert data["neu"] == 0
    assert data["pos"] == 1
    assert data["compound"] == 0.5994

    # les valeurs du score peuvent varier en fonction des versions test les tendances par consequent
    assert data["pos"] >= data["neg"]
    assert data["compound"] > 0