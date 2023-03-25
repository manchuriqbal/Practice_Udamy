from flask import Flask, render_template, request, send_file
import datetime as dt
from geopy.geocoders import Nominatim
import pandas
from geopy.geocoders import options
import os


options.default_user_agent = "app"

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/succes-table", methods=["POST"])
def succes_table():
    global filename
    if request.method == "POST":
        file = request.files["file"]
        try:
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
            filename = dt.datetime.now().strftime("uploads/%Y-%m-%d-%H-%M-%S-%f" + ".csv")
            df.to_csv(filename, index=None)

            return render_template("index.html", text=df.to_html(), btn='download.html')

        except:
            return render_template("index.html", text="Please make sure you have an address column in your CSV file!")


@app.route("/download")
def download():
    return send_file(filename, as_attachment=True, download_name="yourfile.csv")


if "__main__" == __name__:
    app.debug = True
    app.run()
