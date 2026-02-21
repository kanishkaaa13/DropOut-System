# app/routers/predict.py
from fastapi import APIRouter, Depends
from ..schemas import PredictionRequest, PredictionResponse
from ..deps import get_current_user
import joblib
import numpy as np

router = APIRouter(prefix="/predict", tags=["predict"])

rf_model = joblib.load("artifacts/rf_model.joblib")
mlp_model = joblib.load("artifacts/mlp_model.joblib")

class_map = {0: "Dropout", 1: "Enrolled", 2: "Graduate"}  # adjust to your label encoding

def get_risk_level(predicted_class: str) -> str:
    if predicted_class == "Dropout":
        return "High"
    elif predicted_class == "Enrolled":
        return "Medium"
    else:
        return "Low"

@router.post("/", response_model=PredictionResponse)
def predict_outcome(payload: PredictionRequest, user=Depends(get_current_user)):
    # Convert payload to the feature order you used when training
    x = np.array([[
        payload.curricular_units_1st_sem_approved,
        payload.curricular_units_1st_sem_grade,
        payload.curricular_units_2nd_sem_approved,
        payload.curricular_units_2nd_sem_grade,
        payload.admission_grade,
        payload.age_at_enrollment,
        # add rest in same order as training
    ]])

    proba_rf = rf_model.predict_proba(x)[0]
    proba_mlp = mlp_model.predict_proba(x)[0]
    proba_ensemble = (proba_rf + proba_mlp) / 2

    pred_idx = int(np.argmax(proba_ensemble))
    pred_class = class_map[pred_idx]
    risk_level = get_risk_level(pred_class)

    probs_dict = {
        class_map[i]: float(p)
        for i, p in enumerate(proba_ensemble)
    }

    return PredictionResponse(
        predicted_class=pred_class,
        dropout_risk_level=risk_level,
        probabilities=probs_dict,
    )
