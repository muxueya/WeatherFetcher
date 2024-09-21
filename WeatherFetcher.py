import os
from dotenv import load_dotenv
import requests

# Load the environment variables from the .env file
load_dotenv()

# Retrieve the API key from environment variables
API_KEY = os.getenv('OPENWEATHER_API_KEY')

# Base URL of the OpenWeatherMap API for current weather
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'

# City name
city = 'Stockholm'

# Complete the URL
url = BASE_URL + 'q=' + city + '&appid=' + API_KEY + '&units=metric'

# Send HTTP request to the OpenWeatherMap API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    main = data['main']
    wind = data['wind']
    weather_description = data['weather'][0]['description']

    print(f"City: {city}")
    print(f"Temperature: {main['temp']}°C")
    print(f"Humidity: {main['humidity']}%")
    print(f"Pressure: {main['pressure']} hPa")
    print(f"Wind Speed: {wind['speed']} m/s")
    print(f"Weather Description: {weather_description}")
else:
    print("Error in the HTTP request")
