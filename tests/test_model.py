# We will test the model functions here
import sys
sys.path.append("C:\\Users\\GeronimoDUBRA\\Projets\\Dev\\SeriesTemporellesAPI")
from app.utils import fetch_and_process_data
from models.prophet_model import run_prophet

SampleDF=fetch_and_process_data("https://raw.githubusercontent.com/gero007/SeriesTemporellesAPI/refs/heads/main/data/sample.json")
test=run_prophet(SampleDF, "D", 5)
print(test)