import requests
import schedule
import time
from datetime import datetime

API_Key = "40911df8159672644fdbde4c035f4f52"

ville1 = ["Rabat","Casablanca","Tanger","Marrakech","Oujda","Bouarfa"]
ville2 = ["London"]
def recuperer_meteo() :

    print("-" * 50)
    print(f"Mise a Jour : {datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}")
    print("-" * 50)
    for ville in ville1 + ville2 :
        url = f"http://api.openweathermap.org/data/2.5/weather?q={ville}&appid={API_Key}&units=metric"
        response = requests.get(url)
        data = response.json()

        print(f"\nville :", data["name"])
        print(f"Temperature :", data["main"]["temp"], "C")
        print(f"humidite :", data["main"]["humidity"], "%")
        print(f"Etat du ciel:", data["weather"][0]["description"])

schedule.every(1).hours.do(recuperer_meteo)
recuperer_meteo()
print("******")
print("Prochaine Mise a Jour dans 1 heur ")
print("******")

while True :
    schedule.run_pending()
    time.sleep(60)