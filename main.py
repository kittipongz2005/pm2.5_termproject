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
humidity_df = pd.read_csv(os.path.join(data_folder, "humidity_data.csv"))


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


# เพิ่มฟังก์ชั่นสำหรับความชื้น
def assign_color_and_size_humidity(row):
    value = row["Value"]

    # กำหนดสีตามระดับความชื้น
    if value <= 30:
        return "#ff0000", 16  # สีแดง - แห้งมาก
    elif value <= 50:
        return "#ffa500", 14  # สีส้ม - แห้ง
    elif value <= 70:
        return "#ffff00", 12  # สีเหลือง - ปานกลาง
    elif value <= 85:
        return "#7cfc00", 10  # สีเขียว - ชื้น
    else:
        return "#44cef6", 10  # สีฟ้า - ชื้นมาก


# สร้างแอปพลิเคชัน Dash
app = dash.Dash(__name__)

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

# สร้าง CSS สำหรับแถบสีความชื้น
color_scale_humidity = html.Div(
    [
        html.Div(
            style={
                "display": "flex",
                "margin": "10px auto",
                "width": "80%",
                "height": "20px",
            },
            children=[
                html.Div(style={"backgroundColor": "#ff0000", "flex": "1"}),
                html.Div(style={"backgroundColor": "#ffa500", "flex": "1"}),
                html.Div(style={"backgroundColor": "#ffff00", "flex": "1"}),
                html.Div(style={"backgroundColor": "#7cfc00", "flex": "1"}),
                html.Div(style={"backgroundColor": "#44cef6", "flex": "1"}),
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
                html.Div("แห้งมาก (≤30%)"),
                html.Div("แห้ง (≤50%)"),
                html.Div("ปานกลาง (≤70%)"),
                html.Div("ชื้น (≤85%)"),
                html.Div("ชื้นมาก (>85%)"),
            ],
        ),
    ],
    id="color-scale-humidity",
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

# เพิ่มคอลัมน์สีและขนาดใน DataFrame ความชื้น
humidity_df["Value"] = humidity_df["Date1"]
humidity_df["Color"], humidity_df["Size"] = zip(
    *humidity_df.apply(assign_color_and_size_humidity, axis=1)
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
                                src="/assets/air4thai_logo.png",
                                style={"height": "40px"},
                            )
                            if os.path.exists("assets/air4thai_logo.png")
                            else html.H3("Air4Thai")
                        )
                    ],
                    style={"display": "flex", "alignItems": "center"},
                ),
                # เมนูด้านขวา
                html.Div(
                    [
                        html.A(
                            "หน้าหลัก",
                            className="menu-item",
                            style={"margin": "0 15px", "color": "#0078d7"},
                        ),
                        html.A(
                            "รายงาน",
                            className="menu-item",
                            style={"margin": "0 15px", "color": "#0078d7"},
                        ),
                        html.A(
                            "ข้อมูลย้อนหลัง",
                            className="menu-item",
                            style={"margin": "0 15px", "color": "#0078d7"},
                        ),
                        html.A(
                            "เกี่ยวกับคุณภาพอากาศ",
                            className="menu-item",
                            style={"margin": "0 15px", "color": "#0078d7"},
                        ),
                        html.A(
                            "ดาวน์โหลด",
                            className="menu-item",
                            style={"margin": "0 15px", "color": "#0078d7"},
                        ),
                        html.A(
                            "ติดต่อเพิ่มเติม",
                            className="menu-item",
                            style={"margin": "0 15px", "color": "#0078d7"},
                        ),
                        # ปุ่มภาษา
                        html.Button(
                            [
                                (
                                    html.Img(
                                        src="/assets/th_flag.png",
                                        style={"height": "20px", "marginRight": "5px"},
                                    )
                                    if os.path.exists("assets/th_flag.png")
                                    else html.Span("TH", style={"fontWeight": "bold"})
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
                "backgroundColor": "white",
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
                        "width": "100%",
                        "height": "70vh",
                        "border": "1px solid #ddd",
                        "borderRadius": "5px",
                    },
                ),
            ],
            style={"padding": "0 20px", "marginBottom": "15px"},
        ),
        # ส่วนแถบสีทั้งหมด (สร้างตัวแปร)
        color_scale_pm25,
        color_scale_temp,
        color_scale_humidity,
        # ส่วนเลือกประเภทข้อมูล
        html.Div(
            [
                dcc.RadioItems(
                    id="data-type-dropdown",
                    options=[
                        {"label": "PM2.5", "value": "PM2.5"},
                        {"label": "อุณหภูมิ", "value": "Temp"},
                        {"label": "ความชื้น", "value": "Humidity"},
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
        "fontFamily": "Thonburi, Arial, sans-serif",
        "margin": "0",
        "padding": "0",
        "backgroundColor": "#f5f5f5",
    },
)


# Callback เพื่อแสดง/ซ่อนแถบสีตามประเภทข้อมูลที่เลือก
@app.callback(
    [
        Output("color-scale-pm25", "style"),
        Output("color-scale-temp", "style"),
        Output("color-scale-humidity", "style"),
    ],
    [Input("data-type-dropdown", "value")],
)
def toggle_color_scale(data_type):
    pm25_style = {"display": "block"} if data_type == "PM2.5" else {"display": "none"}
    temp_style = {"display": "block"} if data_type == "Temp" else {"display": "none"}
    humidity_style = (
        {"display": "block"} if data_type == "Humidity" else {"display": "none"}
    )

    return pm25_style, temp_style, humidity_style


# Callback เพื่ออัปเดตข้อมูลเมืองและกราฟตามประเภทที่เลือก
@app.callback(
    [Output("thai-map", "figure"), Output("city-info", "children")],
    [Input("data-type-dropdown", "value"), Input("thai-map", "clickData")],
)
def update_map_and_info(data_type, clickData):
    # เลือก DataFrame และฟังก์ชันกำหนดสีตามประเภทข้อมูล
    if data_type == "PM2.5":
        df = pm25_df
        y_label = "ค่า PM2.5 (μg/m³)"
        title_header = "ค่าฝุ่น PM2.5"
        color_assign_func = assign_color_and_size_pm25
    elif data_type == "Temp":
        df = temperature_df
        y_label = "อุณหภูมิ (°C)"
        title_header = "อุณหภูมิ"
        color_assign_func = assign_color_and_size_temp
    elif data_type == "Humidity":
        df = humidity_df
        y_label = "ความชื้น (%)"
        title_header = "ความชื้นสัมพัทธ์"
        color_assign_func = assign_color_and_size_humidity

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
                    "วันที่": date_columns,
                    "ค่า": city_data[date_columns].values.flatten().tolist(),
                }
            )

            # สร้างกราฟเส้น
            fig = px.line(
                plot_data,
                x="วันที่",
                y="ค่า",
                title=f"{title_header}ใน{city}",
                labels={"วันที่": "วันที่", "ค่า": y_label},
            )
            fig.update_traces(mode="lines+markers")
            fig.update_layout(
                xaxis_title="วันที่",
                yaxis_title=y_label,
                template="plotly_white",
                margin={"r": 20, "t": 40, "l": 20, "b": 20},
            )

            return updated_map, html.Div(
                [
                    html.H3(
                        f"เมือง: {city}", style={"marginTop": "20px", "color": "#333"}
                    ),
                    dcc.Graph(figure=fig),
                ]
            )

    return updated_map, city_info


if __name__ == "__main__":
    app.run_server(debug=True)
