import paho.mqtt.client as mqtt
import mysql.connector
import requests
from datetime import datetime, timedelta

# Configuration
API_KEY = "VOTRE_CLE_API"
CITY = "Montbéliard,FR"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
FORECAST_URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"
BROKER = "192.168.1.5"
PORT = 1883

# Connexion à la base de données
def get_last_values_from_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="python",
            password="python",
            database="solaire",
            port=3306
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM prise ORDER BY time DESC LIMIT 3")
        result = cursor.fetchall()
        conn.close()
        return result
    except mysql.connector.Error as err:
        print(f"Erreur: {err}")
        return []

# MQTT - Configuration et publication
def send_mqtt_message(topic, message):
    client = mqtt.Client()
    client.connect(BROKER, PORT)
    client.publish(topic, message)
    print(f"Message envoyé sur {topic}: {message}")
    client.disconnect()

# Obtenir les horaires du lever et du coucher du soleil
def get_sun_times():
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        sunrise = datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.fromtimestamp(data['sys']['sunset'])
        return sunrise, sunset
    return None, None

# Vérifier si nous sommes de jour ou de nuit
def is_daytime(sunrise, sunset):
    current_time = datetime.now()
    return sunrise <= current_time <= sunset

# Vérifier les prévisions météo
def check_weather(sunrise, sunset, threshold_watts):
    response = requests.get(FORECAST_URL)
    if response.status_code == 200:
        data = response.json()
        current_time = datetime.now()
        next_hours = [current_time + timedelta(hours=i) for i in range(1, 4)]

        # Si nous sommes de jour
        if is_daytime(sunrise, sunset):
            print("Nous sommes de jour.")
        else:
            print("Nous sommes de nuit.")

        # Vérification des prévisions pour les 3 prochaines heures
        for forecast in data['list']:
            forecast_time = datetime.fromtimestamp(forecast['dt'])
            if any(next_hour <= forecast_time <= next_hour + timedelta(hours=1) for next_hour in next_hours):
                cloud_coverage = forecast['clouds']['all']
                print(f"Prévision pour {forecast_time.strftime('%H:%M:%S')}: Couverture nuageuse : {cloud_coverage}%")

                # Si la couverture nuageuse est inférieure à 30% et qu'il y a assez de watts
                if cloud_coverage < 30 and threshold_watts > 50:  # Ajustez le seuil des watts ici
                    print("La priorité 2 peut être allumée!")
                    send_mqtt_message("Shelly-Solgaleo/command/switch:1", "on")
                else:
                    print("La priorité 2 ne peut pas être allumée.")
                
        # Vérification de la couverture nuageuse générale
        general_cloud_coverage = data['clouds']['all']
        print(f"Couverture nuageuse générale actuelle : {general_cloud_coverage}%")
        
        if general_cloud_coverage < 30 and threshold_watts > 50:
            print("La priorité 3 peut être allumée!")
            send_mqtt_message("Shelly-Solgaleo/command/switch:2", "on")
        else:
            print("La priorité 3 ne peut pas être allumée.")
    else:
        print("Erreur lors de la récupération des prévisions météo.")

# Fonction principale
def main():
    # Demander les watts à l'utilisateur
    threshold_watts = float(input("Entrez la puissance en watts (pour activer la priorité 2 et 3) : "))

    # Récupérer les derniers enregistrements de la base de données
    db_values = get_last_values_from_db()
    if db_values:
        print("Derniers enregistrements de la base de données :")
        for record in db_values:
            print(record)

    # Récupérer les horaires du soleil
    sunrise, sunset = get_sun_times()
    if sunrise and sunset:
        print(f"Lever du soleil : {sunrise.strftime('%H:%M:%S')}")
        print(f"Coucher du soleil : {sunset.strftime('%H:%M:%S')}")

        # Toujours allumer la prise priorité 1 (Shelly0)
        send_mqtt_message("Shelly-Solgaleo/command/switch:0", "on")

        # Vérifier la météo et les prévisions
        check_weather(sunrise, sunset, threshold_watts)

if __name__ == "__main__":
    main()
