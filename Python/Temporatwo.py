import requests
from datetime import datetime, timedelta

# Clé API et configuration
API_KEY = "2dbc5cd80e3e4ea4f743f832f56ab1c8"
CITY = "Montbéliard,FR"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
FORECAST_URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

# Fonction pour convertir les timestamps UNIX en heure lisible
def format_time(unix_timestamp):
    return datetime.fromtimestamp(unix_timestamp)

# Fonction pour obtenir les horaires de lever/coucher du soleil
def get_sun_times():
    """Récupère les horaires de lever et de coucher du soleil pour Montbéliard."""
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        sunrise = format_time(data['sys']['sunrise'])
        sunset = format_time(data['sys']['sunset'])
        print(f"Lever du soleil : {sunrise.strftime('%H:%M:%S')}")
        print(f"Coucher du soleil : {sunset.strftime('%H:%M:%S')}")
        return sunrise, sunset
    else:
        print(f"Erreur lors de la récupération des données météo : {response.status_code}")
        return None, None

# Fonction pour vérifier si c'est la journée ou la nuit
def is_daytime(sunrise, sunset):
    """Vérifie si nous sommes de jour ou de nuit en fonction des horaires du soleil."""
    current_time = datetime.now()
    if sunrise <= current_time <= sunset:
        return True
    else:
        return False

# Fonction pour vérifier les prévisions météo pour les 3 prochaines heures
def check_weather(sunrise, sunset):
    """Vérifie la météo pour les 3 prochaines heures et affiche la couverture nuageuse."""
    response = requests.get(FORECAST_URL)
    if response.status_code == 200:
        data = response.json()
        current_time = datetime.now()
        next_hours = [current_time + timedelta(hours=i) for i in range(1, 4)]

        # Vérification si c'est le jour ou la nuit
        if is_daytime(sunrise, sunset):
            print("Nous sommes en journée.")
        else:
            print("Nous sommes de nuit.")

        # Vérification des prévisions pour les 3 prochaines heures
        found = False
        for forecast in data['list']:
            forecast_time = datetime.fromtimestamp(forecast['dt'])
            if any(next_hour <= forecast_time <= next_hour + timedelta(hours=1) for next_hour in next_hours):
                cloud_coverage = forecast['clouds']['all']
                print(f"Prévision pour {forecast_time.strftime('%H:%M:%S')}:")
                print(f"  - Couverture nuageuse : {cloud_coverage}%")
                found = True

        if not found:
            print("Aucune prévision météo disponible pour les 3 prochaines heures.")
        
        # Vérification de la couverture nuageuse générale si aucune prévision précise
        if 'clouds' in data['list'][0]:
            general_cloud_coverage = data['list'][0]['clouds']['all']
            print(f"Couverture nuageuse générale actuelle : {general_cloud_coverage}%")

    else:
        print(f"Erreur lors de la récupération des prévisions météo : {response.status_code}")

# Exemple d'utilisation
if __name__ == "__main__":
    sunrise, sunset = get_sun_times()
    if sunrise and sunset:
        check_weather(sunrise, sunset)
