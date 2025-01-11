import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = "84bda36725a6c398f1974f81e7e70f14"
@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    if request.method == "POST":
        city = request.form.get("city")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            wind_deg = data["wind"].get("deg", None)
            def deg_to_compass(deg):
                directions = ['North', 'North-East', 'East', 'South-East', 'South', 'South-West', 'West', 'North-West']
                idx = round(deg / 45) % 8
                return directions[idx]
            weather = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
                "humidity": data["main"]["humidity"],
                "speed": data["wind"]["speed"],
                "feel": data["main"]["feels_like"],
                "direction": deg_to_compass(wind_deg) if wind_deg else "N/A"
            }
        else:
            weather = {"error": "City not found"}
    return render_template("index.html", weather = weather)


if __name__ == "__main__":
    app.run(debug=True)