import mysql.connector
import paho.mqtt.client as mqtt

# Configuration de la base de données
DB_HOST = "localhost"
DB_USER = "python"
DB_PASSWORD = "python"
DB_NAME = "solaire"
DB_PORT = 3306

# Configuration du broker Mosquitto
MQTT_BROKER = "192.168.1.5"
MQTT_PORT = 1883
MQTT_TOPIC = "solaire/prise"

# Connexion à la base de données
def connect_db():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        print("Connexion à la base de données réussie.")
        return connection
    except mysql.connector.Error as err:
        print(f"Erreur : {err}")
        return None

# Réception de données depuis la table "prise"
def fetch_from_prise(connection):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM prise")
        rows = cursor.fetchall()
        print("Données reçues :")
        for row in rows:
            print(row)
        return rows
    except mysql.connector.Error as err:
        print(f"Erreur lors de la récupération : {err}")
        return []

# Envoi de données au broker MQTT
def send_mqtt_message(client, topic, message):
    client.publish(topic, message)
    print(f"Message envoyé au topic {topic} : {message}")

# Programme principal
if __name__ == "__main__":
    # Connexion à la base de données
    db_connection = connect_db()
    if db_connection:
        # Récupérer les données de la table "prise"
        data_rows = fetch_from_prise(db_connection)
        db_connection.close()
        
        # Connexion au broker MQTT
        client = mqtt.Client()
        client.connect(MQTT_BROKER, MQTT_PORT)
        client.loop_start()
        
        # Publier les données récupérées sur MQTT
        for row in data_rows:
            message = f"Plug: {row['plug']}, Time: {row['time']}, Voltage: {row['voltage']}, Current: {row['current']}, Wph: {row['wph']}"
            send_mqtt_message(client, MQTT_TOPIC, message)
        
        # Arrêter le client MQTT
        client.loop_stop()
        client.disconnect()
