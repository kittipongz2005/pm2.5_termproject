from dash import html, dcc  # นำเข้าโมดูล html และ dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from layout import create_initial_graph, create_prediction_cards
from model_001_7days import predict_pm25_arima_001_7days  # นำเข้าโมเดลสำหรับพื้นที่ 1
from model_001_14days import predict_pm25_arima_001_14days  # นำเข้าโมเดลสำหรับพื้นที่ 2
from model_js014_14days import predict_pm25_arima_js014_14days
from model_js014_7days import predict_pm25_arima_js014_7days


def register_callbacks(app):
    @app.callback(
        [Output("prediction_output", "children"), Output("pm25_graph", "figure")],
        [Input("predict_button", "n_clicks")],
        [Input("days_radio", "value")],  # รับค่าจาก RadioItems (7 หรือ 14 วัน)
        [Input("sensor_map", "clickData")],  # รับข้อมูลการคลิกบนแผนที่
    )
    def predict_pm25(n_clicks, days_to_forecast, click_data):
        # หากยังไม่มีการคลิกปุ่ม Predict
        if n_clicks is None or n_clicks == 0:
            return (
                html.Div(
                    "Select a location on the map, choose days, and click 'Predict'",
                    style={"color": "Gold", "fontSize": "1.2rem"},
                ),
                create_initial_graph(),
            )

        # หากยังไม่มีการคลิกบนแผนที่
        if click_data is None:
            return (
                html.Div(
                    "Please click on a location on the map",
                    style={"color": "red", "fontSize": "1.2rem"},
                ),
                create_initial_graph(),
            )

        try:
            # ดึงข้อมูลพื้นที่ที่คลิก
            clicked_location = click_data["points"][0]["text"]  # ดึง ID ของพื้นที่
            print(f"Clicked location: {clicked_location}")

            # ตรวจสอบพื้นที่ที่เลือกและใช้โมเดลที่เหมาะสม
            if clicked_location == "JSPS001":
                if days_to_forecast == 7:
                    predicted_values, future_dates = predict_pm25_arima_001_7days(
                        days_to_forecast
                    )
                elif days_to_forecast == 14:
                    predicted_values, future_dates = predict_pm25_arima_001_14days(
                        days_to_forecast
                    )
            elif clicked_location == "JSPS014":
                if days_to_forecast == 7:
                    predicted_values, future_dates = predict_pm25_arima_js014_7days(
                        days_to_forecast
                    )
                elif days_to_forecast == 14:
                    predicted_values, future_dates = predict_pm25_arima_js014_14days(
                        days_to_forecast
                    )
            else:
                raise ValueError("Invalid location selected")

            # สร้างการ์ดแสดงผลการพยากรณ์
            prediction_cards = create_prediction_cards(predicted_values)

            # สร้างกราฟสำหรับแสดงผลการพยากรณ์
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=future_dates,
                    y=predicted_values,
                    mode="lines",
                    name="Forecast",
                    line=dict(color="var(--primary-color)", width=4),
                )
            )
            fig.update_layout(
                template="plotly_dark",
                xaxis_title="Date",
                yaxis_title="PM2.5 (µg/m³)",
                title=f"PM2.5 Forecast for {clicked_location} ({days_to_forecast} Days)",
                title_font_size=20,
                title_x=0.5,
                plot_bgcolor="var(--secondary-color)",
                paper_bgcolor="var(--secondary-color)",
                font_color="var(--text-color)",
            )

            # คืนค่าการ์ดและกราฟ
            return prediction_cards, fig

        except Exception as e:
            # หากเกิดข้อผิดพลาด
            error_message = f"An error occurred: {str(e)}"
            return (
                html.Div(
                    error_message,
                    style={"color": "red", "fontSize": "1.2rem"},
                ),
                create_initial_graph(),
            )
