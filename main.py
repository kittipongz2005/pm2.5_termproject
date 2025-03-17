from dash import Dash, dcc, html, Input, Output, State, callback_context
import plotly.express as px
import pandas as pd
from model_001 import predict_pm25_arima_001
from model_013 import predict_pm25_arima_013
from model_014 import predict_pm25_arima_014
from model_018 import predict_pm25_arima_018
from model_cha_uat_school import predict_pm25_arima_cha_uat
from model_test_wifi import predict_pm25_arima_test_wifi
from model_001T import predict_temperature_arima_001
from model_013T import predict_temperature_arima_013
from model_014T import predict_temperature_arima_014
from model_018T import predict_temperature_arima_018
from model_cha_uat_schoolT import predict_temperature_arima_cha_uat
from model_test_wifiT import predict_temperature_arima_test_wifi
import os

# สร้าง Dash app
app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1(
            "PM2.5 and Temperature Forecast Dashboard", style={"textAlign": "center"}
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id="data-type-dropdown",
                    options=[
                        {"label": "PM2.5", "value": "pm25"},
                        {"label": "Temperature", "value": "temperature"},
                    ],
                    value="pm25",  # ค่าเริ่มต้น
                    clearable=False,
                    style={"width": "200px", "margin": "10px auto"},
                ),
                dcc.Graph(
                    id="map-graph",
                    config={"scrollZoom": True},
                    style={
                        "height": "60vh",
                        "border": "3px solid black",
                        "borderRadius": "5px",
                        "margin": "0",
                        "padding": "0",
                    },
                ),
                dcc.Graph(
                    id="pm25-graph",
                    style={
                        "display": "none",
                        "height": "40vh",
                        "border": "2px solid black",
                        "borderRadius": "5px",
                        "marginTop": "10px",
                        "padding": "10px",
                    },
                ),
                dcc.Graph(
                    id="temperature-graph",
                    style={
                        "display": "none",
                        "height": "40vh",
                        "border": "2px solid black",
                        "borderRadius": "5px",
                        "marginTop": "10px",
                        "padding": "10px",
                    },
                ),
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
                "gap": "10px",
                "margin": "10px",
                "padding": "10px",
                "width": "90%",
                "maxWidth": "1200px",
                "margin": "0 auto",
            },
        ),
        html.Div(
            [
                html.Div(
                    style={
                        "display": "flex",
                        "margin": "10px auto",
                        "width": "80%",
                        "height": "20px",
                    },
                    children=[
                        html.Div(style={"backgroundColor": "#44cef6", "flex": "1"}),
                        html.Div(style={"backgroundColor": "#7cfc00", "flex": "1"}),
                        html.Div(style={"backgroundColor": "#ffff00", "flex": "1"}),
                        html.Div(style={"backgroundColor": "#ffa500", "flex": "1"}),
                        html.Div(style={"backgroundColor": "#ff0000", "flex": "1"}),
                    ],
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "width": "80%",
                        "margin": "0 auto",
                        "color": "#333",
                        "fontWeight": "bold",
                    },
                    children=[
                        html.Div("ดีมาก"),
                        html.Div("ดี"),
                        html.Div("ปานกลาง"),
                        html.Div("เริ่มมีผลกระทบต่อสุขภาพ"),
                        html.Div("มีผลกระทบต่อสุขภาพ"),
                    ],
                ),
            ],
            id="color-scale-pm25",
            style={"display": "none"},
        ),
        html.Div(
            [
                html.Div(
                    style={
                        "display": "flex",
                        "margin": "10px auto",
                        "width": "80%",
                        "height": "20px",
                    },
                    children=[
                        html.Div(style={"backgroundColor": "#0000FF", "flex": "1"}),
                        html.Div(style={"backgroundColor": "#00FFFF", "flex": "1"}),
                        html.Div(style={"backgroundColor": "#00FF00", "flex": "1"}),
                        html.Div(style={"backgroundColor": "#FFA500", "flex": "1"}),
                        html.Div(style={"backgroundColor": "#FF0000", "flex": "1"}),
                    ],
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "width": "80%",
                        "margin": "0 auto",
                        "color": "#333",
                        "fontWeight": "bold",
                    },
                    children=[
                        html.Div("เย็นมาก"),
                        html.Div("เย็น"),
                        html.Div("ปกติ"),
                        html.Div("ร้อน"),
                        html.Div("ร้อนมาก"),
                    ],
                ),
            ],
            id="color-scale-temperature",
            style={"display": "none"},
        ),
        html.Div(id="weather-cards", style={"display": "none"}),
    ]
)


# ฟังก์ชันกำหนดสีและขนาดของจุดบนแผนที่
def assign_color_and_size_pm25(value):
    if isinstance(value, dict):
        value = value.get("Value", 0)
    if value <= 25:
        return "#44cef6", 10
    elif value <= 50:
        return "#7cfc00", 10
    elif value <= 100:
        return "#ffff00", 12
    elif value <= 150:
        return "#ffa500", 14
    else:
        return "#ff0000", 16


def assign_color_and_size_temperature(value):
    if isinstance(value, dict):
        value = value.get("Value", 0)
    if value <= 15:
        return "#0000FF", 10
    elif value <= 25:
        return "#00FFFF", 10
    elif value <= 30:
        return "#00FF00", 12
    elif value <= 35:
        return "#FFA500", 14
    else:
        return "#FF0000", 16


# ข้อมูลตำแหน่งและโมเดลของแต่ละจุด
locations = [
    {
        "lat": 9.139747579596776,
        "lon": 99.33077139102544,
        "city": "JSPS001",
        "model": predict_pm25_arima_001,
        "temperature_model": predict_temperature_arima_001,
    },
    {
        "lat": 7.02050617186725,
        "lon": 100.48404880020067,
        "city": "JSPS018",
        "model": predict_pm25_arima_018,
        "temperature_model": predict_temperature_arima_018,
    },
    {
        "lat": 7.007446167042591,
        "lon": 100.46894762641548,
        "city": "JSPS013",
        "model": predict_pm25_arima_013,
        "temperature_model": predict_temperature_arima_013,
    },
    {
        "lat": 7.020060006762753,
        "lon": 100.50228426890567,
        "city": "JSPS014",
        "model": predict_pm25_arima_014,
        "temperature_model": predict_temperature_arima_014,
    },
    {
        "lat": 7.007325789671034,
        "lon": 100.10430553665726,
        "city": "R202",
        "model": predict_pm25_arima_test_wifi,
        "temperature_model": predict_temperature_arima_test_wifi,
    },
    {
        "lat": 7.94386,
        "lon": 100.1041,
        "city": "Cha-Uat School",
        "model": predict_pm25_arima_cha_uat,
        "temperature_model": predict_temperature_arima_cha_uat,
    },
]


# Callback เพื่ออัปเดตแผนที่และแสดงกราฟ PM2.5 Forecast หรือ Temperature Forecast
@app.callback(
    [
        Output("map-graph", "figure"),
        Output("pm25-graph", "figure"),
        Output("temperature-graph", "figure"),
        Output("pm25-graph", "style"),
        Output("temperature-graph", "style"),
        Output("color-scale-pm25", "style"),
        Output("color-scale-temperature", "style"),
        Output("weather-cards", "children"),
        Output("weather-cards", "style"),
    ],
    [Input("map-graph", "clickData"), Input("data-type-dropdown", "value")],
)
def update_map_and_graph(click_data, data_type):
    # สร้าง DataFrame สำหรับแผนที่
    map_df = pd.DataFrame(locations)

    if data_type == "pm25":
        # ทำนายค่า PM2.5 สำหรับแต่ละจุด
        map_df["Value"] = [model(7)[0][0] for model in map_df["model"]]
        map_df["Color"], map_df["Size"] = zip(
            *map_df["Value"].apply(assign_color_and_size_pm25)
        )
    else:
        # ทำนายค่าอุณหภูมิสำหรับแต่ละจุด
        map_df["Value"] = [loc["temperature_model"](7)[0][0] for loc in locations]
        map_df["Color"], map_df["Size"] = zip(
            *map_df["Value"].apply(assign_color_and_size_temperature)
        )

    # สร้างแผนที่แบบ scattermapbox
    map_fig = px.scatter_mapbox(
        map_df,
        lat="lat",
        lon="lon",
        hover_name="city",
        color="Color",
        size="Size",
        size_max=15,
        zoom=5,
        height=500,
    )

    if click_data:
        lat = click_data["points"][0]["lat"]
        lon = click_data["points"][0]["lon"]
        map_fig.update_layout(
            mapbox_style="open-street-map",
            mapbox=dict(center=dict(lat=lat, lon=lon)),
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            showlegend=False,
        )

        city = click_data["points"][0]["hovertext"]
        selected_location = next(loc for loc in locations if loc["city"] == city)

        if data_type == "pm25":
            predicted_values, future_dates = selected_location["model"](7)
            df = pd.DataFrame(
                {"Date": future_dates, "Predicted PM2.5": predicted_values}
            )
            pm25_fig = px.line(
                df,
                x="Date",
                y="Predicted PM2.5",
                title=f"PM2.5 Forecast for {city}",
                markers=True,
                labels={"Predicted PM2.5": "PM2.5 (µg/m³)"},
            )
            pm25_fig.update_layout(
                xaxis_title="Date", yaxis_title="PM2.5 (µg/m³)", template="plotly_white"
            )
            temperature_fig = {}
            pm25_style = {"display": "block"}
            temperature_style = {"display": "none"}
            color_scale_pm25_style = {"display": "block"}
            color_scale_temperature_style = {"display": "none"}
        else:
            predicted_values, future_dates = selected_location["temperature_model"](7)
            df = pd.DataFrame(
                {"Date": future_dates, "Predicted Temperature": predicted_values}
            )
            temperature_fig = px.line(
                df,
                x="Date",
                y="Predicted Temperature",
                title=f"Temperature Forecast for {city}",
                markers=True,
                labels={"Predicted Temperature": "Temperature (°C)"},
            )
            temperature_fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Temperature (°C)",
                template="plotly_white",
            )
            pm25_fig = {}
            pm25_style = {"display": "none"}
            temperature_style = {"display": "block"}
            color_scale_pm25_style = {"display": "none"}
            color_scale_temperature_style = {"display": "block"}

        # สร้าง Weather Cards
        thai_days = ["อา.", "จ.", "อ.", "พ.", "พฤ.", "ศ.", "ส."]
        weather_cards = html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    thai_days[i % 7], style={"fontWeight": "bold"}
                                ),
                                html.Div(
                                    html.Div(
                                        style={
                                            "width": "50px",
                                            "height": "50px",
                                            "borderRadius": "50%",
                                            "backgroundColor": (
                                                assign_color_and_size_pm25(
                                                    {"Value": predicted_values[i]}
                                                )[0]
                                                if data_type == "pm25"
                                                else assign_color_and_size_temperature(
                                                    {"Value": predicted_values[i]}
                                                )[0]
                                            ),
                                            "margin": "10px auto",
                                        }
                                    ),
                                ),
                                html.Div(
                                    [
                                        html.Span(
                                            f"{round(predicted_values[i])} {'µg/m³' if data_type == 'pm25' else '°C'}",
                                            style={
                                                "fontWeight": "bold",
                                                "fontSize": "20px",
                                            },
                                        ),
                                    ]
                                ),
                            ],
                            style={
                                "backgroundColor": "#f8f9fa",
                                "borderRadius": "8px",
                                "padding": "15px",
                                "margin": "5px",
                                "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                                "width": "100px",
                                "textAlign": "center",
                            },
                        )
                        for i in range(len(predicted_values))
                    ],
                    style={
                        "display": "flex",
                        "justifyContent": "center",
                        "flexWrap": "wrap",
                        "margin": "20px 0",
                    },
                )
            ]
        )

        weather_cards_style = {"display": "block"}

    else:
        map_fig.update_layout(
            mapbox_style="open-street-map",
            mapbox=dict(center=dict(lat=13.7563, lon=100.5018)),
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            showlegend=False,
        )

        pm25_fig = {}
        temperature_fig = {}
        pm25_style = {"display": "none"}
        temperature_style = {"display": "none"}
        color_scale_pm25_style = {"display": "none"}
        color_scale_temperature_style = {"display": "none"}
        weather_cards = None
        weather_cards_style = {"display": "none"}

    return (
        map_fig,
        pm25_fig,
        temperature_fig,
        pm25_style,
        temperature_style,
        color_scale_pm25_style,
        color_scale_temperature_style,
        weather_cards,
        weather_cards_style,
    )


# รันแอป
if __name__ == "__main__":
    app.run_server(debug=True)
