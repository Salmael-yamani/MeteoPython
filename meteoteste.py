

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
        print("on peut pas de connecter a MySQL")
        return
    cursor = connexion.cursor()

    for ville in ville1 + ville2 :
        url = f"http://api.openweathermap.org/data/2.5/weather?q={ville}&appid={API_Key}&units=metric"
        response = requests.get(url)
        data = response.json()

        print(f"\nville :", data["name"])
        print(f"Temperature :", data["main"]["temp"], "C")
        print(f"humidite :", data["main"]["humidity"], "%")
        print(f"Etat du ciel:", data["weather"][0]["description"])


        requete = """ insert into historique_meteo ( ville , Temperature, humidite, descriptions, temp_min, temp_max)
        VALUES (%s, %s, %s, %s, %s, %s)  
        """
        valeurs = (
            ville_nom ,
            temperature ,
            humidite ,
            descriptions ,
            temp_min ,
            temp_max
        )
        cursor.execute(requete , valeurs)
        connexion.commit()
        print(f"Les donnees enregistrees dans MySQL")



schedule.every(1).hours.do(recuperer_meteo)
recuperer_meteo()
print("******")
print("Prochaine Mise a Jour dans 1 heur ")
print("******")

while True :
    schedule.run_pending()
    time.sleep(60)





















