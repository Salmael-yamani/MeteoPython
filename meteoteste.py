from idlelib.sidebar import temp_enable_text_widget
from logging import exception

import requests
import schedule
import time
from datetime import datetime
import mysql.connector
from mysql.connector import Error


API_Key = "40911df8159672644fdbde4c035f4f52"

config_mysql = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Salma2003',
    'database': 'meteo_db'
}

#listes
ville1 = ["Rabat","Casablanca","Tanger","Marrakech","Oujda","Bouarfa"]
ville2 = ["London"]

def creer_connexion():
    try :
        connexion = mysql.connector.connect(**config_mysql)
        return connexion
    except Error as e:
        print(f"Il y a un erreur de connexion : {e}")
        return None

def recuperer_meteo() :

    print("-" * 50)
    print(f"Mise a Jour : {datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}")
    print("-" * 50)

    connexion = creer_connexion()
    if not connexion :
        print("on ne peut pas de connecter a MySQL")
        return
    cursor = connexion.cursor()
    succes = 0

    erreurs = 0

    for ville in ville1 + ville2 :
       try :

           url = f"http://api.openweathermap.org/data/2.5/weather?q={ville}&appid={API_Key}&units=metric"
           response = requests.get(url)
           data = response.json()

           ville_nom = data["name"]
           temperature = data["main"]["temp"]
           humidite = data["main"]["humidity"]
           descriptions = data["weather"][0]["description"]
           temp_min = data["main"]["temp_min"]
           temp_max = data["main"]["temp_max"]



           print(f"\nville : {ville_nom}")
           print(f"Température  : {temperature} °C")
           print(f"Humidité : {humidite} %")
           print(f"État du ciel : {descriptions}" )


           requete = """ insert into historique_meteo ( ville , Temperature, humidite, descriptions, temp_min, temp_max)
           VALUES (%s, %s, %s, %s, %s, %s)  
        """
           valeurs = (
               ville_nom,
               temperature,
               humidite,
               descriptions,
               temp_min,
               temp_max
           )

           cursor.execute(requete, valeurs)
           connexion.commit()
           print(f"Les donnees sont  enregistrees dans MySQL")
           succes += 1

       except exception as e :
           print(f"il y a un erreur pour {ville} : {e}")
           erreurs += 1

    cursor.close()
    connexion.close()














schedule.every(1).hours.do(recuperer_meteo)
recuperer_meteo()
print("******")
print("Prochaine Mise a Jour dans 1 heur ")
print("******")

while True :
    schedule.run_pending()
    time.sleep(60)





















