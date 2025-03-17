import pandas as pd
import numpy as np
from pycaret.time_series import load_model, predict_model

# โหลดโมเดลที่ train ไว้
model = load_model("Temp013")

# โหลดข้อมูล forecast
forecast = pd.read_csv("Temp013_predic.csv")
forecast["timestamp"] = pd.to_datetime(forecast["timestamp"])
forecast.set_index("timestamp", inplace=True)
forecast.index = forecast.index.to_period("D")

# ทำการพยากรณ์
predictions = predict_model(model, X=forecast)


def predict_temperature_arima_013(days_to_forecast):
    """
    ทำการพยากรณ์อุณหภูมิจากโมเดลที่โหลดไว้
    โดยดึงข้อมูลจากตัวแปร predictions และทำนายตามจำนวนวันที่เลือก
    """
    # ดึงข้อมูลที่พยากรณ์ไว้แล้วจาก predictions
    predicted_values = predictions["y_pred"].tail(days_to_forecast).values
    future_dates = predictions.index[-days_to_forecast:].to_timestamp()

    return predicted_values, future_dates
