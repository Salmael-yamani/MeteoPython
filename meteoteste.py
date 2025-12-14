'''import requests

API_KEY = "40911df8159672644fdbde4c035f4f52"
ville = "Rabat"
ville = "Marrakech"

url = f"http://api.openweathermap.org/data/2.5/weather?q={ville}&appid={API_KEY}&units=metric"

response = requests.get(url)
data = response.json()

print(data) '''
import requests

API_KEY = "40911df8159672644fdbde4c035f4f52"
ville = "Rabat"

url = f"http://api.openweathermap.org/data/2.5/weather?q={ville}&appid={API_KEY}&units=metric"

response = requests.get(url)
data = response.json()

print("Ville :", data["name"])
print("Température :", data["main"]["temp"], "°C")
print("Humidité :", data["main"]["humidity"], "%")
print("État du ciel :", data["weather"][0]["description"])

