import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from flask import Flask, render_template

# เริ่มต้น Flask server
server = Flask(__name__)

# เริ่มต้น Dash app
app = dash.Dash(__name__, server=server, routes_pathname_prefix="/dashboard/")

# อ่านข้อมูลจากไฟล์ CSV
df = pd.read_csv("data/pm25_data.csv")

# สร้างกราฟจากข้อมูล (ตัวอย่าง: กราฟ PM2.5)
fig = px.line(df, x="Time", y="PM2.5", title="PM2.5 Over Time")

# กำหนด Layout ของ Dash
app.layout = html.Div(
    [
        html.H1("PM2.5 Dashboard", style={"text-align": "center"}),
        dcc.Graph(id="pm25-graph", figure=fig),
        html.P("แสดงข้อมูล PM2.5 จากไฟล์ CSV"),
    ]
)


@server.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    server.run(debug=True)
