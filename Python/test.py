from database import connect_to_db
from add_data import add_plug, add_scenario, add_power_consumption

def get_all_consumption():
    """Récupère toutes les consommations pour chaque prise."""
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    
    # Récupérer toutes les valeurs de consommation pour chaque prise
    cursor.execute('''
        SELECT plug, time, wph 
        FROM power_consumption
        WHERE plug IN ('Shelly0', 'Shelly1', 'Meross')
        ORDER BY plug, time
    ''')
    
    result = cursor.fetchall()
    db.close()
    
    # Afficher les résultats pour déboguer
    print("Toutes les consommations récupérées :")
    for row in result:
        print(f"{row['plug']} à {row['time']} : {row['wph']}W")
    
    # Retourner un dictionnaire avec la consommation pour chaque prise
    consumption_data = {}
    for row in result:
        if row['plug'] not in consumption_data:
            consumption_data[row['plug']] = []
        consumption_data[row['plug']].append(row['wph'])
    
    return consumption_data


# Tester la fonction de récupération
get_last_consumption()
