from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd  # เพิ่ม import pandas
from model_001 import predict_pm25_arima_001

# สร้าง Dash app
app = Dash(__name__)

# Layout ของแอป
app.layout = html.Div(
    [
        html.H1("PM2.5 Forecast Dashboard", style={"textAlign": "center"}),
        html.Label("จำนวนวันที่ต้องการทำนาย:"),
        dcc.Input(
            id="days-to-forecast", type="number", value=7, min=1, max=30
        ),  # กำหนดช่วงวันที่ทำนาย
        dcc.Graph(id="pm25-forecast-graph"),
    ]
)


# Callback เพื่ออัปเดตกราฟเมื่อผู้ใช้เปลี่ยนจำนวนวันที่ทำนาย
@app.callback(
    Output("pm25-forecast-graph", "figure"), Input("days-to-forecast", "value")
)
def update_graph(days_to_forecast):
    # ดึงค่าที่ทำนายไว้
    predicted_values, future_dates = predict_pm25_arima_001(days_to_forecast)

    # สร้าง DataFrame สำหรับ Plotly
    df = pd.DataFrame({"Date": future_dates, "Predicted PM2.5": predicted_values})

    # สร้างกราฟด้วย Plotly Express
    fig = px.line(
        df,
        x="Date",
        y="Predicted PM2.5",
        title=f"PM2.5 Forecast for the next {days_to_forecast} days",
        markers=True,
        labels={"Predicted PM2.5": "PM2.5 (µg/m³)"},
    )
    fig.update_layout(
        xaxis_title="Date", yaxis_title="PM2.5 (µg/m³)", template="plotly_white"
    )
    return fig


# รันแอป
if __name__ == "__main__":
    app.run_server(debug=True)
