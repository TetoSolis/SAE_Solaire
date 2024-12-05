import paho.mqtt.client as mqtt

# Configuration du broker
BROKER = "192.168.1.5"
PORT = 1883
TOPIC = "#"

# Callback pour la réception des messages
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()
    print(f"Topic: {topic} | Message: {payload}")

# Configuration du client MQTT
client = mqtt.Client()
client.on_message = on_message

# Connexion au broker et abonnement au wildcard "#"
client.connect(BROKER, PORT)
client.subscribe(TOPIC)

print(f"Abonné à tous les topics ('{TOPIC}'). En attente de messages...")
client.loop_forever()
