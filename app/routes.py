from fastapi import APIRouter, HTTPException
from app.utils import fetch_and_process_data
from models.prophet_model import run_prophet
import os
import json
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/predict/")
async def predict(
    remote_url: str,
    scale: str ,
    periods: int = 10
):
    """
    Récupérer les données de séries temporelles à partir d'une URL et exécuter le modèle Prophet pour la prédiction.
    Args:
        remote_url (str): URL pour récupérer les données de séries temporelles.
        scale (str, optionnel): Échelle de temps (par exemple, 'quotidien', 'mensuel', 'annuel'). Par défaut à None.
        periods (int): Nombre de périodes à prévoir.

    Returns:
        dict: Données originales et prédites au format JSON.
    """
    try:
        # Fetch and process data
        df = fetch_and_process_data(remote_url)
        # Run Prophet model
        result = run_prophet(df, scale, periods)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/sample-data/")
async def get_sample_data():
    """
    Servir un fichier JSON d'exemple pour les tests.
    Returns:
        JSON: Données de séries temporelles d'exemple.
    """
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sample_data_path = os.path.join(ROOT_DIR, "data", "sample.json")
    try:
        with open(sample_data_path, "r") as f:
            data = json.load(f)
        return JSONResponse(content=data)
    except FileNotFoundError:
        return JSONResponse(content={"error": "Sample data not found."}, status_code=404)