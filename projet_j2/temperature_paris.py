import requests

# Récupération de la température actuelle à Paris
url = "https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522&current_weather=true"
response = requests.get(url)
data = response.json()
temperature = data['current_weather']['temperature']

print(f"La température actuelle à Paris est de {temperature}°C")