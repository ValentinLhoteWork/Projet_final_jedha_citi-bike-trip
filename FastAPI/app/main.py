from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

from app.prediction import predict_from_user_date

# ---------------------------------

# Création de l'application

# ---------------------------------

app = FastAPI(
title="Citi Bike Net Flow Prediction API",
description="API for predicting Citi Bike station net flow",
version="1.0.0"
)

# ---------------------------------

# Chargement des données

# ---------------------------------

import pandas as pd

dataset_fe = pd.read_parquet(
"data/historical_data.parquet"
)

# ---------------------------------

# Features utilisées par le modèle

# ---------------------------------

features = [
"station_id",
"year",
"month",
"day",
"hour",
"temp",
"precipitation_total",
"relative_humidity",
"average_wind_speed",
"num_bikes_taken_lag_1",
"num_bikes_dropped_lag_1",
"net_flow_lag_1",
"net_flow_lag_2",
"net_flow_lag_24",
"net_flow_roll_3",
"net_flow_roll_24",
"jour_semaine",
"coco_group",
"is_holiday",
"coco"
]

# ---------------------------------

# Colonnes mises à jour avec

# les données météo / calendrier

# ---------------------------------

update_columns = [
"temp",
"relative_humidity",
"precipitation_total",
"average_wind_speed",
"coco",
"coco_group",
"is_holiday"
]

# ---------------------------------

# Modèle de requête

# ---------------------------------

PredictionRequest = type(
    "PredictionRequest",
    (BaseModel,),
    {
        "__annotations__": {
            "station_id": str,
            "datetime": datetime
        }
    }
)
    


# ---------------------------------

# Route principale

# ---------------------------------

@app.get("/")
def root():
    return {
        "message": "Citi Bike Net Flow Prediction API",
        "status": "running"
}


# ---------------------------------

# Endpoint de prédiction

# ---------------------------------

@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        prediction = predict_from_user_date(
            dataset=dataset_fe,
            request_datetime=request.datetime,
            features=features,
            model_path="model/citibike_forecast_model.joblib",
            station_id=request.station_id,
            update_columns=update_columns
            )
        if prediction is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"No historical data available for "
                    f"station {request.station_id} "
                    f"at the requested time."
                    )
                )
        return {
            "station_id": request.station_id,
            "datetime": request.datetime,
            "predicted_net_flow": round(float(prediction), 2)
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
            )

