import paho.mqtt.client as mqtt
# Configuration
BROKER = "192.168.1.5"
PORT = 1883
TOPIC = "Shelly-Solgaleo/command/switch:1"
MESSAGE = "on"

# Configuration du client
client = mqtt.Client()

# Connexion au broker
client.connect(BROKER, PORT)

# Publier un message
client.publish(TOPIC, MESSAGE)
print(f"Message envoyé : {MESSAGE}")

client.disconnect()
