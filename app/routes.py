from fastapi import APIRouter, HTTPException
from models.prophet_model import run_prophet
import os
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
from typing import List, Dict

router = APIRouter()

# Input schema for the endpoint
class PredictRequest(BaseModel):
    period: int
    scale: str
    data: List[Dict[str, float]]

@router.post("/predict/")
async def predict(request: PredictRequest):
    """
    Récupérer les données de séries temporelles à partir des données fournies et exécuter le modèle Prophet pour la prédiction.
    Args:
        request (PredictRequest): Données d'entrée pour la prédiction, y compris la période, l'échelle et les données de séries temporelles.

    Returns:
        dict: Données originales et prédites au format JSON.
    """
    try:
        # Convert the input data to a DataFrame
        data_dict = {}
        for entry in request.data:
            for date, value in entry.items():
                data_dict[date] = value

        # Convert to DataFrame
        df = pd.DataFrame(list(data_dict.items()), columns=["ds", "y"])
        df["ds"] = pd.to_datetime(df["ds"], errors="raise")

        # Check and convert the 'ds' column
        try:
            df['ds'] = pd.to_datetime(df['ds'], errors='raise')
        except Exception as e:
            raise ValueError(f"Invalid date formats found. Error: {e}")

        # Run the prediction
        result = run_prophet(df, request.scale, request.period)
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