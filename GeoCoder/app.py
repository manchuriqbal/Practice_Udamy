from flask import Flask, render_template, request, send_file
import datetime as dt
from geopy.geocoders import Nominatim
import pandas
from geopy.geocoders import options
import os


options.default_user_agent = "my-application"

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/succes-table", methods=["POST"])
def succes_table():
    if request.method == "POST":
        file = request.files["file"]
        df = pandas.read_csv(file)
        gc = Nominatim(user_agent="app")
        df['coordinates'] = df["Address"].apply(gc.geocode)
        df['Latitude'] = df["coordinates"].apply(
            lambda x: x.latitude if x != None else None)
        df['Longitude'] = df["coordinates"].apply(
            lambda x: x.longitude if x != None else None)
        df = df.drop("coordinates", axis=1)
        directory = "uploads"
        if not os.path.exists(directory):
            os.makedirs(directory)
        df.to_csv("uploads/geocodeed.csv", index=None)

        return render_template("index.html", text=df.to_html(), btn='download.html')


@app.route("/download")
def download():
    return send_file("uploads/geocodeed.csv", download_name="yourname.csv", as_attachment=True)


if "__main__" == __name__:
    app.debug = True
    app.run()
