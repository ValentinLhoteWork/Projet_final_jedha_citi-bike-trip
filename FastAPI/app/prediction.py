import joblib
import pandas as pd
import holidays

from app.weather import get_weather

MODEL_PATH = "model/citibike_forecast_model.joblib"

def predict_from_user_date(
dataset,
request_datetime,
features,
station_id,
update_columns
):
    


# ---------------------------------
# Charger le modèle
# ---------------------------------
    model = joblib.load(MODEL_PATH)
    df = dataset.copy()
    request_datetime = pd.to_datetime(
        request_datetime
        )
    month_req = request_datetime.month
    dow_req = request_datetime.dayofweek
    hour_req = request_datetime.hour

# ---------------------------------
# Reconstruire date_hour
# ---------------------------------

    df["date_hour"] = pd.to_datetime(
        df[["year", "month", "day", "hour"]]
        )

# ---------------------------------
# Chercher les données historiques
# correspondant au mois,
# jour de semaine et heure
# ---------------------------------

    df_filtered = df[
        (df["date_hour"].dt.month == month_req) &
        (df["date_hour"].dt.dayofweek == dow_req) &
        (df["date_hour"].dt.hour == hour_req)
        ]

# ---------------------------------
# Filtrer par station
# ---------------------------------

    df_filtered = df_filtered[
        df_filtered["station_id"] == station_id
        ]

# ---------------------------------
# Aucune donnée historique
# ---------------------------------

    if df_filtered.empty:
        return None

# ---------------------------------
# Prendre l'observation historique
# la plus récente
# ---------------------------------

    df_filtered = df_filtered.sort_values(
        "date_hour"
        )
    X = df_filtered[
        features
        ].iloc[-1:].copy()

# ---------------------------------
# Récupérer la météo actuelle
# ---------------------------------

    weather_df = get_weather(
        request_datetime
        )

# ---------------------------------
# Mise à jour météo
# ---------------------------------

    for col in update_columns:

        if (
            col in X.columns
            and col in weather_df.columns
            ):
            X.loc[:, col] = weather_df[
                col].iloc[0]

# ---------------------------------
# Holiday
# ---------------------------------

    us_holidays = holidays.US(
        years=request_datetime.year
        )

    if "is_holiday" in X.columns:

        X.loc[:, "is_holiday"] = int(
            request_datetime.date()
            in us_holidays
            )

# ---------------------------------
# Prediction
# ---------------------------------

    prediction = model.predict(X)[0]
    return prediction

