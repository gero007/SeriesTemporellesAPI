from prophet import Prophet
import pandas as pd

from prophet import Prophet
import pandas as pd

def run_prophet(df: pd.DataFrame, scale: str, periods: int) -> dict:
    """Run Prophet prediction on the given DataFrame."""
    try:

        # Initialiser et ajuster le modèle
        model = Prophet()
        model.fit(df)

        # Générer des dates futures
        future = model.make_future_dataframe(periods=periods, freq=scale)

        # Prédire uniquement pour les périodes futures
        forecast = model.predict(future)
        future_forecast = forecast.iloc[-periods:]

        # Combiner les données originales et prédites
        result = df[['ds', 'y']].copy()
        result['type'] = 'original'

        future_result = future_forecast[['ds']].copy()
        future_result['y'] = future_forecast['yhat']
        future_result['type'] = 'prévu'

        combined_result = pd.concat([result, future_result], ignore_index=True)

        return combined_result.to_dict(orient='records')
    except Exception as e:
        raise ValueError(f"Erreur dans le modèle Prophet: {str(e)}")
    
