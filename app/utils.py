import pandas as pd
import requests
from fastapi import HTTPException


def fetch_and_process_data(url: str) -> pd.DataFrame:
    """
    Récupère les données d'une URL distante et les convertit en DataFrame.

    Cette fonction envoie une requête HTTP GET à l'URL spécifiée, 
    récupère les données au format JSON et les convertit en un DataFrame pandas.
    Les données doivent contenir les colonnes 'ds' et 'y'. Si ces colonnes ne sont pas présentes,
    une exception est levée.

    Args:
        url (str): L'URL de laquelle récupérer les données.

    Returns:
        pd.DataFrame: Un DataFrame pandas contenant les données récupérées.

    Raises:
        HTTPException: Si une erreur survient lors de la récupération des données ou si les colonnes 'ds' et 'y' ne sont pas présentes.
    """
    """Fetch data from a remote URL and convert to a DataFrame."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        df = pd.DataFrame(json_data)
        if 'ds' not in df.columns or 'y' not in df.columns:
            raise ValueError("Data must contain 'ds' and 'y' columns.")
        return df
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching data: {str(e)}")