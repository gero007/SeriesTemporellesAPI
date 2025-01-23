import sys
sys.path.append("C:\\Users\\GeronimoDUBRA\\Projets\\Dev\\SeriesTemporellesAPI")
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)  # Définir le client pour effectuer des requêtes

def test_predict_with_sample_data():
    # Étape 1 : Récupérer les données d'exemple
    response = client.get("/sample-data/")  # Utiliser le client pour appeler le point de terminaison
    assert response.status_code == 200
    sample_data = response.json()

    # Étape 2 : Envoyer les données d'exemple au point de terminaison de prédiction
    payload = {
        "remote_url": "https://raw.githubusercontent.com/gero007/SeriesTemporellesAPI/refs/heads/main/data/sample.json",
        "scale": "D",
        "periods": 5
    }

        # URL template
    url_template = "http://localhost:8000/predict/?remote_url={remote_url}&scale={scale}&periods={periods}"

    # Construct URL using f-string
    url = url_template.format(
        remote_url=payload["remote_url"],
        scale=payload["scale"],
        periods=payload["periods"]
    )
    response = client.get(url)  # Post à prediction
    assert response.status_code == 200

test_predict_with_sample_data()