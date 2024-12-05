import mysql.connector

def connect_to_db():
    """Retourne la connexion à la base de données."""
    return mysql.connector.connect(
        host="localhost",
        user="python",
        password="python",
        database="solaire"
    )

def create_tables():
    """Crée les tables nécessaires si elles n'existent pas."""
    db = connect_to_db()
    cursor = db.cursor()
    
    # Table pour les scénarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scenarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            max_power INT,
            max_plugs INT,
            cloud_coverage INT
        )
    ''')
    
    # Table pour les prises
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plugs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            plug_name VARCHAR(50),
            priority INT
        )
    ''')
    
    # Table pour la consommation d'énergie
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS power_consumption (
            id INT AUTO_INCREMENT PRIMARY KEY,
            plug VARCHAR(50),
            time DATETIME,
            voltage FLOAT,
            current FLOAT,
            wph FLOAT
        )
    ''')

    db.commit()
    db.close()
