from prophet import Prophet
import pandas as pd
from dateutil import parser

def run_prophet(df: pd.DataFrame, scale: str, periods: int) -> dict:
    """Run Prophet prediction on the given DataFrame."""
    try:
        # Detect the input date format
        sample_date = df['ds'].iloc[0]
        input_date_format = parser.parse(str(sample_date)).strftime('%Y-%m-%d')

        # Initialize and fit the model
        model = Prophet()
        model.fit(df)

        # Generate future dates
        future = model.make_future_dataframe(periods=periods, freq=scale)
        forecast = model.predict(future)

        # Separate future predictions
        future_forecast = forecast.iloc[-periods:]

        # Prepare the "Original" section
        original = [{"ds": row["ds"], "y": row["y"]} for _, row in df.iterrows()]
        original = [{str(item["ds"].date()): item["y"]} for item in original]

        # Prepare the "Predicted" section
        predicted = [{"ds": row["ds"], "yhat": row["yhat"]} for _, row in future_forecast.iterrows()]
        predicted = [{str(item["ds"].date()): item["yhat"]} for item in predicted]

        # Combine results into desired format
        result = {
            "Original": original,
            "Predicted": predicted
        }
        return result
        return response
    except Exception as e:
        raise ValueError(f"Error in Prophet model: {str(e)}")
