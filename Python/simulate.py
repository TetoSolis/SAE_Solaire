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

def simulate_scenario(scenario_id):
    """Simule l'état des prises pour un scénario donné."""
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    
    # Obtenir les détails du scénario
    cursor.execute('SELECT * FROM scenarios WHERE id = %s', (scenario_id,))
    scenario = cursor.fetchone()
    
    # Obtenir toutes les consommations des prises
    all_consumption = get_all_consumption()
    
    # Trier les prises par priorité
    cursor.execute('SELECT * FROM plugs ORDER BY priority')
    plugs = cursor.fetchall()
    
    # Calculer l'état des prises en fonction du scénario
    max_power = scenario['max_power']
    used_plugs = 0
    state = []
    total_consumption = 0  # Pour calculer la consommation totale
    cloud_coverage = scenario['cloud_coverage']  # Couverture nuageuse du scénario
    
    for plug in plugs:
        plug_name = plug['plug_name']
        priority = plug['priority']
        consumption = sum(all_consumption.get(plug_name, []))  # Consommation totale pour cette prise
        
        # Gérer les prises selon leur priorité
        if priority == 1:
            state.append(f"{plug_name} - Allumée")
            used_plugs += 1
            total_consumption += consumption
        elif priority == 2:
            if cloud_coverage <= 30:  # Si couverture nuageuse <= 30%, allumer la prise
                if used_plugs < scenario['max_plugs'] and max_power >= consumption:
                    state.append(f"{plug_name} - Allumée pendant 1 heure")
                    used_plugs += 1
                    total_consumption += consumption
                    max_power -= consumption
            else:
                state.append(f"{plug_name} - Éteinte (couverture nuageuse trop élevée)")
        elif priority == 3 and used_plugs < scenario['max_plugs'] and max_power >= consumption:
            state.append(f"{plug_name} - Allumée (priorité 3)")
            used_plugs += 1
            total_consumption += consumption
            max_power -= consumption
        else:
            state.append(f"{plug_name} - Éteinte")
    
    # Afficher l'état des prises
    print(f"Scénario {scenario_id}:")
    for line in state:
        print(line)
    
    # Afficher la consommation totale utilisée pour ce scénario
    print(f"Consommation totale utilisée pour ce scénario : {total_consumption}W")
    
    db.close()
