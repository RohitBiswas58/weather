from django.shortcuts import render
import requests
from datetime import datetime, timedelta

def home(request):
    city = request.GET.get('city', 'Dum Dum')
    api_key = ''
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    try:
        data = requests.get(url).json()
        timezone_offset = data.get('timezone', 0)
        local_timezone = timedelta(seconds=timezone_offset)

        local_time = datetime.utcfromtimestamp(data['dt']) + local_timezone
        formatted_time = local_time.strftime('%H:%M:%S')
        
        sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise']) + local_timezone
        sunset_time = datetime.utcfromtimestamp(data['sys']['sunset']) + local_timezone

    
        weather = {
            'city': data.get('name', 'N/A'),
            'country': data['sys'].get('country', 'N/A'),
            'coordinates': {'lon': data['coord']['lon'], 'lat': data['coord']['lat']},
            'weather': data['weather'][0]['main'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'temperature': {
                'kelvin': data['main']['temp'],
                'celsius': int(data['main']['temp'] - 273.15),
                'feels_like_celsius': int(data['main']['feels_like'] - 273.15),
                'min_celsius': int(data['main']['temp_min'] - 273.15),
                'max_celsius': int(data['main']['temp_max'] - 273.15),
            },
            'pressure': data['main']['pressure'],
            'humidity': data['main']['humidity'],
            'sea_level': data['main'].get('sea_level', 'N/A'),
            'ground_level': data['main'].get('grnd_level', 'N/A'),
            'visibility': data.get('visibility', 'N/A'),
            'wind': {
                'speed': data['wind']['speed'],
                'degree': data['wind']['deg']
            },
            'clouds': data['clouds']['all'],
            'timezone_offset': timezone_offset,
            'local_time': formatted_time,
            'sunrise': sunrise_time.strftime('%H:%M:%S'),
            'sunset': sunset_time.strftime('%H:%M:%S'),
        }
    except (KeyError, IndexError, requests.RequestException):
        weather = {
            'city': 'N/A',
            'country': 'N/A',
            'coordinates': {'lon': 'N/A', 'lat': 'N/A'},
            'weather': 'N/A',
            'description': 'N/A',
            'icon': 'N/A',
            'temperature': {
                'kelvin': 'N/A',
                'celsius': 'N/A',
                'feels_like_celsius': 'N/A',
                'min_celsius': 'N/A',
                'max_celsius': 'N/A',
            },
            'pressure': 'N/A',
            'humidity': 'N/A',
            'sea_level': 'N/A',
            'ground_level': 'N/A',
            'visibility': 'N/A',
            'wind': {
                'speed': 'N/A',
                'degree': 'N/A'
            },
            'clouds': 'N/A',
            'timezone_offset': 'N/A',
            'local_time': 'N/A',
            'sunrise': 'N/A',
            'sunset': 'N/A',
        }

    context = {'data': weather}
    return render(request, 'home.html', context)
