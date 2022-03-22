import random
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render

import requests


def random_user_agents():
    """returns random user-agents from the list"""
    UA = user_agent_list = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    ]

    return random.choice(UA)


def today_weather(request):
    data_json = {
        "coord": {"lon": 35.7374, "lat": -0.2479},
        "weather": [
            {
                "id": 804,
                "main": "Clouds",
                "description": "overcast clouds",
                "icon": "04d"
            }
        ],
        "base": "stations",
        "main": {
            "temp": 25,
            "feels_like": 24.1,
            "temp_min": 25,
            "temp_max": 25,
            "pressure": 1010,
            "humidity": 21,
            "sea_level": 1010,
            "grnd_level": 767
        },
        "visibility": 10000,
        "wind": {"speed": 5, "deg": 47, "gust": 3.66},
        "clouds": {"all": 100},
        "dt": 1647424872,
        "sys": {"country": "KE", "sunrise": 1647402147, "sunset": 1647445750},
        "timezone": 10800,
        "id": 186315,
        "name": "Molo",
        "cod": 200
    }
    data = {}
    if request.method == "POST":
        save_data = request.POST.get("save_data", None)
        city_name = request.POST.get("city")
        
        headers = {"User-Agent": random_user_agents()}
        
        try:
            # send request
            OPENWEATHER_API_KEY =settings.OPENWEATHER_API_KEY
            response = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHER_API_KEY}&units=metric",
                headers=headers
            )
            data_json = response.json()
        
            if response.status_code == 200:
                data = {
                    "country_code": data_json["sys"]["country"],
                    "coord": str(data_json['coord']["lon"]) + ", " + str(data_json['coord']["lat"]),
                    "temp_max": data_json['main']['temp_max'],
                    "temp_min": data_json['main']['temp_min'],
                    "temp_feels": data_json["main"]["feels_like"],
                    "pressure": data_json["main"]['pressure'],
                    "humidity": data_json['main']['humidity'],
                    "main": data_json['weather'][0]['main'],
                    "desc": data_json['weather'][0]['description'],
                    "icon": data_json['weather'][0]['icon'],
                    "name": data_json["name"],
                    "wind": data_json["wind"]['speed']
                }
                if save_data:
                    print("data will be save in the database")
                else:
                    print("data will not be save in the database")
            else:
                messages.error(request, data_json["message"])
        except requests.ConnectionError:
            messages.error(request, "Unable to reach Weather data provider. Ensure you have internet connection")
    else:
        data = {
            "country_code": data_json["sys"]["country"],
            "coord": str(data_json['coord']["lon"]) + ", " + str(data_json['coord']["lat"]),
            "temp_max": data_json['main']['temp_max'],
            "temp_min": data_json['main']['temp_min'],
            "temp_feels": data_json["main"]["feels_like"],
            "pressure": data_json["main"]['pressure'],
            "humidity": data_json['main']['humidity'],
            "main": data_json['weather'][0]['main'],
            "desc": data_json['weather'][0]['description'],
            "icon": data_json['weather'][0]['icon'],
            "name": data_json["name"],
            "wind": data_json["wind"]['speed']
        }
            
    return render(request, "weather/index.html", data)
