from flask import Flask, render_template, request
import requests
import pycountry
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os



load_dotenv()
# api_key = os.getenv('WEATHER_API_KEY')
api_key = "d1a359d9370352e8e8dd1ccb889ab489"


def country_name_to_code(name):
    try:
        country = pycountry.countries.lookup(name)
        return country.alpha_2  # returns the 2-letter country code
    except LookupError:
        return None

def country_code_to_name(code):
    try:
        country = pycountry.countries.get(alpha_2=code.upper())
        return country.name
    except:
        return None

def deg_to_compass(deg):
    directions = ["N","NE","E","SE","S","SW","W","NW"]
    ix = int((deg + 22.5) / 45) % 8
    return directions[ix]


app = Flask(__name__, template_folder="Templates", static_folder="Statics")

@app.route('/', methods=["POST", "GET"])

@app.route('/', methods=["POST", "GET"])
def index():
    error_message = None
    weather_data = None   # initialize here

    if request.method == 'POST':
        country = request.form["country"].strip()
        city = request.form["city"].strip()

        if not country or not city:
            error_message = "Please enter both the city and country to get weather report!"
        else:
            country_code = country_name_to_code(country)
            if not country_code:
                error_message = "Country not found. Please check spellings!"
            else:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={api_key}&units=metric"
                try:
                    response = requests.get(url, timeout=5)
                    data = response.json()

                    if int(data.get("cod")) != 200:
                        msg = data.get("message", "Unable to fetch weather data!").capitalize()
                        if msg == "City not found":
                            error_message = "City not found. Please check spellings!"
                        else:
                            error_message = msg
                    
                    
                    else:
                        weather_data = {
                            "city": data["name"],
                            "country": country_code_to_name(data["sys"]["country"]),
                            "temp": data["main"]["temp"],
                            "feels_like": data["main"]["feels_like"],
                            "description": data["weather"][0]["description"].title(),
                            "humidity": data["main"]["humidity"],
                            "pressure": data["main"]["pressure"],  # hPa
                            "clouds": data["clouds"]["all"],       # %
                            "visibility": data["visibility"] / 1000,  # km
                            "wind_speed": data["wind"]["speed"],
                            "wind_dir": deg_to_compass(data["wind"]["deg"]),
                            "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"] + data["timezone"]).strftime("%I:%M %p"),
                            "sunset": datetime.fromtimestamp(data["sys"]["sunset"] + data["timezone"]).strftime("%I:%M %p"),
                        }

                except requests.exceptions.RequestException:
                    error_message = "Weather Service is Unavailable. Try again later!"

    return render_template('index.html', weather_info=weather_data, error_message=error_message)


if __name__ == "__main__":
    app.run(debug=False)
