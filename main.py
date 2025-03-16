import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import os

# กำหนด path ของโฟลเดอร์ data
data_folder = "data"

# อ่านไฟล์ CSV จากโฟลเดอร์ data
pm25_df = pd.read_csv(os.path.join(data_folder, "pm25_data.csv"))
temperature_df = pd.read_csv(os.path.join(data_folder, "temperature_data.csv"))


# เพิ่มคอลัมน์สีและขนาดสำหรับการแสดงผลบนแผนที่
def assign_color_and_size_pm25(row):
    value = row["Value"]  # สมมติว่ามีคอลัมน์ Value ที่เก็บค่าล่าสุด

    # กำหนดสีตามระดับค่า PM2.5 (ตามแถบสีในภาพ)
    if value <= 25:
        return "#44cef6", 10  # สีฟ้า - ดีมาก
    elif value <= 50:
        return "#7cfc00", 10  # สีเขียว - ดี
    elif value <= 100:
        return "#ffff00", 12  # สีเหลือง - ปานกลาง
    elif value <= 150:
        return "#ffa500", 14  # สีส้ม - เริ่มมีผลกระทบ
    else:
        return "#ff0000", 16  # สีแดง - มีผลกระทบ


# เพิ่มฟังก์ชั่นสำหรับอุณหภูมิ
def assign_color_and_size_temp(row):
    value = row["Value"]

    # กำหนดสีตามระดับอุณหภูมิ
    if value <= 20:
        return "#44cef6", 10  # สีฟ้า - เย็น
    elif value <= 25:
        return "#7cfc00", 10  # สีเขียว - เย็นสบาย
    elif value <= 30:
        return "#ffff00", 12  # สีเหลือง - อุ่น
    elif value <= 35:
        return "#ffa500", 14  # สีส้ม - ร้อน
    else:
        return "#ff0000", 16  # สีแดง - ร้อนมาก


# สร้างแอปพลิเคชัน Dash
app = dash.Dash(__name__)
app.title = "Air Quality Insights"  # เปลี่ยนชื่อแอปพลิเคชัน

# สร้าง CSS สำหรับแถบสี PM2.5
color_scale_pm25 = html.Div(
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
)

# สร้าง CSS สำหรับแถบสีอุณหภูมิ
color_scale_temp = html.Div(
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
                html.Div("เย็น (≤20°C)"),
                html.Div("เย็นสบาย (≤25°C)"),
                html.Div("อุ่น (≤30°C)"),
                html.Div("ร้อน (≤35°C)"),
                html.Div("ร้อนมาก (>35°C)"),
            ],
        ),
    ],
    id="color-scale-temp",
    style={"display": "none"},
)

# เพิ่มคอลัมน์สีและขนาดใน DataFrame สำหรับการแสดงผลครั้งแรก
pm25_df["Value"] = pm25_df["Date1"]  # ใช้ค่าล่าสุดเป็นตัวกำหนดสี
pm25_df["Color"], pm25_df["Size"] = zip(
    *pm25_df.apply(assign_color_and_size_pm25, axis=1)
)

# เพิ่มคอลัมน์สีและขนาดใน DataFrame อุณหภูมิ
temperature_df["Value"] = temperature_df["Date1"]
temperature_df["Color"], temperature_df["Size"] = zip(
    *temperature_df.apply(assign_color_and_size_temp, axis=1)
)

# สร้างแผนที่แบบ scattermapbox ด้วย Plotly สำหรับ PM2.5 (เริ่มต้น)
map_fig = px.scatter_mapbox(
    pm25_df,
    lat="Lat",
    lon="Lon",
    hover_name="City",
    color_discrete_map="identity",
    color="Color",
    size="Size",
    size_max=15,
    zoom=5,
    height=500,
)

map_fig.update_layout(
    mapbox_style="open-street-map",
    mapbox=dict(
        center=dict(lat=13.7563, lon=100.5018), zoom=5  # ตั้งค่าจุดศูนย์กลางที่กรุงเทพฯ
    ),
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    showlegend=False,
)

# Layout ของแอป
app.layout = html.Div(
    [
        # ส่วนหัว (Header)
        html.Div(
            [
                html.Div(
                    [
                        (
                            html.Img(
                                src="/assets/logo.png",
                                style={"height": "40px"},
                            )
                            if os.path.exists("assets/logo.png")
                            else html.H3("Air Quality Insights")
                        )
                    ],
                    style={"display": "flex", "alignItems": "center"},
                ),
                # เมนูด้านขวา
                html.Div(
                    [
                        html.A(
                            "Home",
                            className="menu-item",
                            style={"margin": "0 15px", "color": "#0078d7"},
                        ),
                        html.A(
                            "Reports",
                            className="menu-item",
                            style={"margin": "0 15px", "color": "#0078d7"},
                        ),
                        html.A(
                            "Historical Data",
                            className="menu-item",
                            style={"margin": "0 15px", "color": "#0078d7"},
                        ),
                        html.A(
                            "About Air Quality",
                            className="menu-item",
                            style={"margin": "0 15px", "color": "#0078d7"},
                        ),
                        html.A(
                            "Download",
                            className="menu-item",
                            style={"margin": "0 15px", "color": "#0078d7"},
                        ),
                        html.A(
                            "Contact Us",
                            className="menu-item",
                            style={"margin": "0 15px", "color": "#0078d7"},
                        ),
                        # ปุ่มภาษา
                        html.Button(
                            [
                                (
                                    html.Img(
                                        src="/assets/en_flag.png",
                                        style={"height": "20px", "marginRight": "5px"},
                                    )
                                    if os.path.exists("assets/en_flag.png")
                                    else html.Span("EN", style={"fontWeight": "bold"})
                                )
                            ],
                            style={
                                "border": "none",
                                "background": "none",
                                "cursor": "pointer",
                                "display": "flex",
                                "alignItems": "center",
                            },
                        ),
                    ],
                    style={"display": "flex", "alignItems": "center"},
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "padding": "10px 20px",
                "borderBottom": "1px solid #ddd",
                "backgroundColor": "#f8f9fa",
                "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
            },
        ),
        html.Div(
            [html.P("  ")],
        ),
        # ส่วนแผนที่
        html.Div(
            [
                dcc.Graph(
                    id="thai-map",
                    figure=map_fig,
                    config={"scrollZoom": True},
                    style={
                        "width": "70%",
                        "height": "70vh",
                        "border": "1px solid #ddd",
                        "border": "3px solid black",
                        "borderRadius": "5px",
                    },
                ),
            ],
            style={
                "padding": "0 20px",
                "marginBottom": "15px",
                "display": "flex",
                "justifyContent": "center",  # จัดให้อยู่ตรงกลาง
            },
        ),
        # ส่วนแถบสีทั้งหมด (สร้างตัวแปร)
        color_scale_pm25,
        color_scale_temp,
        # ส่วนเลือกประเภทข้อมูล
        html.Div(
            [
                dcc.RadioItems(
                    id="data-type-dropdown",
                    options=[
                        {"label": "PM2.5", "value": "PM2.5"},
                        {"label": "Temperature", "value": "Temp"},
                    ],
                    value="PM2.5",
                    labelStyle={
                        "display": "inline-block",
                        "marginRight": "20px",
                        "fontSize": "16px",
                    },
                    style={"textAlign": "center", "margin": "20px 0"},
                ),
            ],
            style={"width": "80%", "margin": "auto"},
        ),
        # ส่วนแสดงข้อมูลเมืองเมื่อคลิก
        html.Div(id="city-info", style={"width": "80%", "margin": "auto"}),
    ],
    style={
        "fontFamily": "Arial, sans-serif",
        "margin": "0",
        "padding": "0",
        "backgroundColor": "#e9ecef",
    },
)


# Callback เพื่อแสดง/ซ่อนแถบสีตามประเภทข้อมูลที่เลือก
@app.callback(
    [
        Output("color-scale-pm25", "style"),
        Output("color-scale-temp", "style"),
    ],
    [Input("data-type-dropdown", "value")],
)
def toggle_color_scale(data_type):
    pm25_style = {"display": "block"} if data_type == "PM2.5" else {"display": "none"}
    temp_style = {"display": "block"} if data_type == "Temp" else {"display": "none"}
    return pm25_style, temp_style


# Callback เพื่ออัปเดตข้อมูลเมืองและกราฟตามประเภทที่เลือก
@app.callback(
    [Output("thai-map", "figure"), Output("city-info", "children")],
    [Input("data-type-dropdown", "value"), Input("thai-map", "clickData")],
)
def update_map_and_info(data_type, clickData):
    # เลือก DataFrame และฟังก์ชันกำหนดสีตามประเภทข้อมูล
    if data_type == "PM2.5":
        df = pm25_df
        y_label = "PM2.5 Value (μg/m³)"
        title_header = "PM2.5 Levels"
        color_assign_func = assign_color_and_size_pm25
    elif data_type == "Temp":
        df = temperature_df
        y_label = "Temperature (°C)"
        title_header = "Temperature"
        color_assign_func = assign_color_and_size_temp

    # อัปเดตค่าสีและขนาดตามข้อมูลที่เลือก
    df["Value"] = df["Date1"]  # ใช้ค่าล่าสุดเป็นตัวกำหนดสี
    df["Color"], df["Size"] = zip(*df.apply(color_assign_func, axis=1))

    # ตั้งค่าค่าเริ่มต้นสำหรับ map center และ zoom level
    center_lat = 13.7563  # ค่าเริ่มต้นที่กรุงเทพฯ
    center_lon = 100.5018
    zoom_level = 5  # ค่าเริ่มต้น

    # ถ้ามีการคลิกที่จุด ให้ซูมไปที่จุดนั้น
    if clickData is not None:
        center_lat = clickData["points"][0]["lat"]
        center_lon = clickData["points"][0]["lon"]
        zoom_level = 8  # ซูมเข้าเล็กน้อย (ค่ายิ่งมากยิ่งซูมเข้า)

    # สร้างแผนที่ใหม่
    updated_map = px.scatter_mapbox(
        df,
        lat="Lat",
        lon="Lon",
        hover_name="City",
        color_discrete_map="identity",
        color="Color",
        size="Size",
        size_max=15,
        zoom=zoom_level,  # ใช้ค่า zoom_level ที่คำนวณไว้
        height=500,
    )

    updated_map.update_layout(
        mapbox_style="open-street-map",
        mapbox=dict(center=dict(lat=center_lat, lon=center_lon), zoom=zoom_level),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        showlegend=False,
    )

    # ข้อมูลเมืองเมื่อคลิก
    city_info = html.Div()
    if clickData is not None:
        city = clickData["points"][0]["hovertext"]
        city_data = df[df["City"] == city]

        if not city_data.empty:
            # กรองเฉพาะคอลัมน์ Date1 ถึง Date7 เท่านั้น
            date_columns = [col for col in city_data.columns if col.startswith("Date")][
                :7
            ]

            # สร้าง DataFrame ใหม่เพื่อนำไปพล็อตกราฟ
            plot_data = pd.DataFrame(
                {
                    "Date": date_columns,
                    "Value": city_data[date_columns].values.flatten().tolist(),
                }
            )

            # สร้างกราฟเส้น
            fig = px.line(
                plot_data,
                x="Date",
                y="Value",
                title=f"{title_header} in {city}",
                labels={"Date": "Date", "Value": y_label},
            )
            fig.update_traces(mode="lines+markers")
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title=y_label,
                template="plotly_white",
                margin={"r": 20, "t": 40, "l": 20, "b": 20},
            )

            # สร้างตารางข้อมูลแต่ละวันในรูปแบบคล้ายพยากรณ์อากาศ
            # สร้างวันที่แบบไทย
            thai_days = ["อา.", "จ.", "อ.", "พ.", "พฤ.", "ศ.", "ส."]

            # สร้าง weather card container
            weather_cards = html.Div(
                [
                    html.Div(
                        [
                            # สร้าง weather card สำหรับแต่ละวัน
                            html.Div(
                                [
                                    html.Div(
                                        thai_days[i % 7], style={"fontWeight": "bold"}
                                    ),
                                    # เพิ่มไอคอนตามความเหมาะสม
                                    html.Div(
                                        html.Div(
                                            style={
                                                "width": "50px",
                                                "height": "50px",
                                                "borderRadius": "50%",
                                                "backgroundColor": (
                                                    assign_color_and_size_pm25(
                                                        {
                                                            "Value": city_data[
                                                                col
                                                            ].values[0]
                                                        }
                                                    )[0]
                                                    if data_type == "PM2.5"
                                                    else assign_color_and_size_temp(
                                                        {
                                                            "Value": city_data[
                                                                col
                                                            ].values[0]
                                                        }
                                                    )[0]
                                                ),
                                                "margin": "10px auto",
                                            }
                                        ),
                                    ),
                                    # แสดงค่าที่เหมาะสมตามประเภทข้อมูล
                                    html.Div(
                                        [
                                            html.Span(
                                                (
                                                    f"{round(city_data[col].values[0])}°"
                                                    if data_type == "Temp"
                                                    else f"{round(city_data[col].values[0])} μg/m³"
                                                ),
                                                style={
                                                    "fontWeight": "bold",
                                                    "fontSize": "20px",
                                                },
                                            ),
                                            html.Span(" "),
                                            # แสดงค่าที่เหมาะสมตามประเภทข้อมูล (ถ้ามี)
                                            html.Span(
                                                get_secondary_value(
                                                    city_data, col, data_type
                                                ),
                                                style={
                                                    "color": "#777",
                                                    "fontSize": "16px",
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
                            for i, col in enumerate(date_columns)
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

            return updated_map, html.Div(
                [
                    html.H3(
                        f"City: {city}", style={"marginTop": "20px", "color": "#333"}
                    ),
                    dcc.Graph(figure=fig),
                    html.H4(
                        "Daily Data",
                        style={
                            "marginTop": "20px",
                            "color": "#333",
                            "textAlign": "center",
                        },
                    ),
                    weather_cards,
                ]
            )

    return updated_map, city_info


def get_secondary_value(city_data, col, data_type):
    """สร้างค่าที่สอง (ถ้ามี) สำหรับแสดงในการ์ดพยากรณ์"""
    # กรณีอุณหภูมิ แสดงค่าต่ำสุด (สมมติว่าหาได้จากการลบ 5-10 องศา)
    if data_type == "Temp":
        high_temp = city_data[col].values[0]
        low_temp = max(high_temp - 8, 0)  # ลดลง 8 องศา แต่ไม่ต่ำกว่า 0
        return f"{round(low_temp)}°"
    else:
        return ""  # ไม่แสดงค่าที่สองสำหรับข้อมูลอื่น


if __name__ == "__main__":
    app.run_server(debug=True)
