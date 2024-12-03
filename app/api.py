from pathlib import Path
import numpy as np
from fastapi import FastAPI, Response
from joblib import load
from .schemas import Loan, Rating, feature_names
from .monitoring import instrumentator
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError



ROOT_DIR = Path(__file__).parent.parent

app = FastAPI()
scaler = load(ROOT_DIR / "artifacts/scaler.joblib")
model = load(ROOT_DIR / "artifacts/model.joblib")

instrumentator.instrument(app).expose(app, include_in_schema=False, should_gzip=True)


@app.get("/")
def root():
    return "loan status Ratings"

# response_model : target
# sample : Feature
@app.post("/predict" , response_model= Rating)
def predict(response: Response, sample: Loan):
    sample_dict = sample.dict()
    features = np.array([sample_dict[f] for f in feature_names]).reshape(1, -1)
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]
  
    response.headers["X-model-score"] = str(prediction)
    return Rating(loan_status=prediction)


@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )