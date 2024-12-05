import mysql.connector

# Configuration de la base de données
DB_CONFIG = {
    "host": "localhost",
    "user": "python",
    "password": "python",
    "database": "solaire",
    "port": 3306,
}

# Fonction pour récupérer les dernières valeurs de chaque prise avec calcul de la puissance instantanée
def get_latest_values_with_power():
    """Récupère la dernière valeur pour chaque prise et calcule la puissance instantanée."""
    query = """
    SELECT plug, MAX(time) AS latest_time, voltage, current, (voltage * current) AS power
    FROM prise
    WHERE time = (
        SELECT MAX(time) 
        FROM prise AS inner_table 
        WHERE inner_table.plug = prise.plug
    )
    GROUP BY plug;
    """

    try:
        # Connexion à la base de données
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()

        # Afficher les résultats
        print("Dernières valeurs pour chaque prise avec puissance instantanée :")
        for row in results:
            print(f"{row['plug']} - Temps : {row['latest_time']}, Voltage : {row['voltage']} V, "
                  f"Courant : {row['current']} A, Puissance Instantanée : {row['power']} W")
        
        # Fermeture de la connexion
        cursor.close()
        connection.close()
    except mysql.connector.Error as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")

# Exemple d'utilisation
if __name__ == "__main__":
    get_latest_values_with_power()
