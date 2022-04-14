import requests
from datetime import *
from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

# environment variable - I don't want to expose my api key in git, that's why I am uploading the api
# key from .emv. I would make git ignore this file that contains my api key
load_dotenv()

# Initialize application
app = Flask(__name__)


# home page
@app.route('/')
def index():
    return render_template('index.html')


# Results page
@app.route('/results', methods=['GET', 'POST'])  # Results page
def render_results():
    city = request.form['city_name']
    app_id = os.getenv("app_id") #extract api from env file
    URL = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={app_id}'
    res = requests.get(URL).json()  # Creating variables to transfer to results page
    print("MY DATA", res)
    country = res['sys']['country']
    humidity = res['main']['humidity']
    temp = res['main']['temp']
    feels_like = res['main']['feels_like']
    wind_speed = res['wind']['speed']
    condition = res['weather'][0]['main']

    time_stamp = res['dt']
    date_time = datetime.fromtimestamp(time_stamp)
    current_hour = date_time.strftime("%H")  # extract the current hour in X city

    sunrise = res['sys']['sunrise']
    sunrise_time = datetime.fromtimestamp(sunrise)
    sunrise_hour = sunrise_time.strftime("%H")  # extract the sunrise hour

    sunset = res['sys']['sunset']
    sunset_time = datetime.fromtimestamp(sunset)
    sunset_hour = sunset_time.strftime("%H")  # extract the sunset hour

    # changing the animation according to the condition (9 possibilities)
    svg_folder = '/static/animated/'
    if (condition == 'Clear') and (sunrise_hour < current_hour < sunset_hour):  # CLEAR SKY DAY
        svg_file = 'day.svg'
    if (condition == 'Clear') and (current_hour > sunset_hour):  # CLEAR SKY NIGHT
        svg_file = 'night.svg'
    if (condition == 'Clouds') and (sunrise_hour < current_hour < sunset_hour):  # CLOUDY DAY
        svg_file = 'cloudy.svg'
    if (condition == 'Clouds') and (current_hour > sunset_hour):  # CLOUDY NIGHT
        svg_file = 'cloudy-night-3.svg'
    if (condition == 'Snow') and (sunrise_hour < current_hour < sunset_hour):  # SNOWY DAY
        svg_file = 'snowy-3.svg'
    if (condition == 'Snow') and (current_hour > sunset_hour):  # SNOWY NIGHT
        svg_file = 'snowy-6.svg'
    if (condition == 'Rain') and (sunrise_hour < current_hour < sunset_hour):  # RAINY DAY
        svg_file = 'rainy-3.svg'
    if (condition == 'Rain') and (current_hour > sunset_hour):  # RAINY NIGHT
        svg_file = 'rainy-6.svg'
    if (condition == 'Rain') and (sunrise_hour < current_hour < sunset_hour):  # Thunderstorm DAY/NIGHT
        svg_file = 'thunder.svg'

    # creating the route for flask to get to the right animation (svg file)
    svg_file = svg_folder + svg_file

    # Returning the values to the '/results' page
    return render_template('results.html', city=city.title(), country=country, humidity=humidity,
                           condition=condition, temp=round(temp), feels_like=round(feels_like),
                           wind_speed=round(wind_speed), svg_file=svg_file)
    # transfer the data by jinja2 method {{}} to html files


if __name__ == '__main__':
    app.run()
