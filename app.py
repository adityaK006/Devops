from flask import Flask, render_template, request
import requests
from config import API_KEY
from db import init_db, insert_search, get_last_searches

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    history = get_last_searches()

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            try:
                response = requests.get(url)
                print("Requesting URL:", url)
                print("Status code:", response.status_code)
                print("Response:", response.text)

                if response.status_code == 200:
                    weather_data = response.json()
                    insert_search(city)  # Save searched city to DB
                    history = get_last_searches()  # Update history after insert
                else:
                    weather_data = {"error": "City not found."}
            except Exception as e:
                weather_data = {"error": "Failed to fetch weather data."}
                print("Error:", e)

    return render_template("index.html", weather=weather_data, history=history)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5001, debug=True) 
