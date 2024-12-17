from pathlib import Path
import numpy as np
from fastapi import FastAPI,Response
from joblib import load
from .schemas import Loan, Rating, feature_names
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import pandas as pd
import pickle

ROOT_DIR = Path(__file__).parent.parent

app = FastAPI()
model = load(ROOT_DIR / "artifacts/model.joblib")


@app.get("/")
def root():
    return "loan status Ratings"


@app.post("/predict", response_model= Rating)
def predict(response: Response, sample: Loan):

    sample_df = pd.DataFrame([dict(sample)])
    #features = np.array([sample[f] for f in feature_names]).reshape(1, -1) 
    #features_scaled = scaler.transform(features)
 
    prediction = model.predict(sample_df)[0]
    
    response.headers["X-model-score"] = str(prediction)   
    return {"target": prediction}

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

