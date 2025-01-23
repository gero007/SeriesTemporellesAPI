import sys
sys.path.append("C:\\Users\\GeronimoDUBRA\\Projets\\Dev\\SeriesTemporellesAPI")
from fastapi import FastAPI
from app.routes import router


app = FastAPI(title="Time Series Prediction API", version="1.0.0")

# Include the routes from the router
app.include_router(router)