from flask import Flask, render_template, request
import requests
import pycountry
from dotenv import load_dotenv
from datetime import datetime
import os


load_dotenv()
api_key = os.getenv('WEATHER_API_KEY')
print(api_key)

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

app = Flask(__name__, template_folder="Templates", static_folder="Statics")

@app.route('/', methods=["POST", "GET"])
def index():
    error_message = None
    weather_info = None
    if request.method == 'POST':
        country = request.form["country"].strip()
        city = request.form["city"].strip()
        print(city, country)
        
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
                    weather_data = response.json()
                    print(f"'{weather_data}'")
                    
                    if int(weather_data.get("cod")) != 200 and int(weather_data.get("cod")) != 404:
                        error_message = "Unable to fetch weather data. Please try again later!"
                    elif int(weather_data.get('cod')) == 404:
                        error_message = "City not found. Please check spellings!"
                    else:
                        weather_info ={
                            "city": weather_data['name'],
                            "country": country_code_to_name(weather_data['sys']['country']),
                            "temp": weather_data['main']['temp'],
                            "feels_like" : weather_data["main"]['feels_like'], 
                            "min" : weather_data["main"]['temp_max'],
                            'max': weather_data["main"]['temp_min'],
                            "sunrise" : datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime("%H:%M:%S"),
                            "sunset" : datetime.fromtimestamp(weather_data['sys']['sunset']).strftime("%H:%M:%S"),
                            "description": weather_data['weather'][0]['description'],
                            "humidity": weather_data['main']['humidity'],
                            "wind_speed": weather_data['wind']['speed']
                        }
                except requests.exceptions.RequestException:
                    error_message = "Weather Service is Unavailable. Try again later!"



    return render_template('index.html', weather_info = weather_info, error_message = error_message)

if __name__ == "__main__":
    app.run(debug=True)
