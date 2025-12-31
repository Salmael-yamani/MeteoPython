

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
'''
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
        print("on ne peut pas se connecter a MySQL")
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

       except Exception as e :
           print(f"il y a une erreur pour {ville} : {e}")
           erreurs += 1



    cursor.close()
    connexion.close()



schedule.every(1).hours.do(recuperer_meteo)
recuperer_meteo()


print("******")
print("Prochaine Mise a Jour dans 1 heur ")
print("******")'''






###partie 2
def creer_connexion():

    try :
        connexion = mysql.connector.connect(**config_mysql)
        return connexion
    except Error as e:
        print(f"Il y a une erreur de connexion : {e}")
        return None

def choix_de_utilisateur() :

    print("Bienvenue ")
    ville_demandee = input("🌍 entrez le nom d'une ville : ")

    if not ville_demandee :
        print("nom de ville vide ")
        return True


    try :
        url_actuel = f"http://api.openweathermap.org/data/2.5/weather?q={ville_demandee}&appid={API_Key}&units=metric"
        response_actuel = requests.get(url_actuel)

        if response_actuel.status_code == 404:
            print(f"la ville n'exsit pas ou un faute d'ortographe ")
            return True
        elif response_actuel.status_code == 429:
            print(f"attendez quelques secondes ")
            return True
        elif response_actuel.status_code != 200:
            print(f"impossible de recuperer les donnees ")
            return True


        data_actuel = response_actuel.json()

        ville_nom = data_actuel["name"]
        temperature = data_actuel["main"]["temp"]
        temp_min = data_actuel["main"]["temp_min"]
        temp_max = data_actuel["main"]["temp_max"]
        humidite = data_actuel["main"]["humidity"]
        descriptions = data_actuel["weather"][0]["description"]
        vitesse_vent = data_actuel["wind"]["speed"]


        url_forecast = f"http://api.openweathermap.org/data/2.5/forecast?q={ville_demandee}&appid={API_Key}&units=metric"
        response_forecast = requests.get(url_forecast)
        data_forecast = response_forecast.json()


        probabilite_pluie = 0
        if response_forecast.status_code == 200:
            data_forecast = response_forecast.json()
            if "list" in data_forecast:
                previsions = data_forecast["list"]
                if len(previsions) > 0:
                    premiere_prevision = previsions[0]
                    pop = premiere_prevision.get("pop", 0)
                    probabilite_pluie = int(pop * 100)

        print("-" * 50)
        print(f"Mise a Jour : {datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}")
        print("-" * 50)

        print(f" Ville - {ville_nom.upper() : ^7} ")
        print(f"Température  : {temperature} °C")
        print(f"📉 Température min : {temp_min}°C")
        print(f"📈 Température max : {temp_max}°C")
        print(f"Humidité : {humidite} %")
        print(f"État du ciel : {descriptions}")
        print(f" vitesse du vent : {vitesse_vent}")
        print(f"Probablite de pluie :{probabilite_pluie}")

        connexion = creer_connexion()
        if connexion :
            cursor = connexion.cursor()

            requete_insert = """
            insert into utilisateur_mete
            (ville , temperature , temp_min , temp_max , humidite , descriptions )
            VALUES (%s, %s, %s, %s, %s, %s)"""
            valeurs = (
                ville_nom,
                temperature,
                humidite,
                descriptions,
                temp_min,
                temp_max
            )
            cursor.execute(requete_insert, valeurs)
            connexion.commit()

            print("les donnees dont enregistree dans MySQL")

        return True





    except Exception as e :
        print(f"erreur : {e}")
        return True





if __name__ == "__main__":

    try:
            continuer = True
            while True :
                continuer=choix_de_utilisateur()
                time.sleep(2)

    except KeyboardInterrupt:
        print(f"AU revoir ")
    print("le programme est termine ")





























