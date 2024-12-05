from database import connect_to_db

def add_scenario(max_power, max_plugs, cloud_coverage):
    """Ajoute un scénario dans la base de données."""
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO scenarios (max_power, max_plugs, cloud_coverage)
        VALUES (%s, %s, %s)
    ''', (max_power, max_plugs, cloud_coverage))
    db.commit()
    db.close()

def add_plug(plug_name, priority):
    """Ajoute une prise dans la base de données."""
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO plugs (plug_name, priority)
        VALUES (%s, %s)
    ''', (plug_name, priority))
    db.commit()
    db.close()

def add_power_consumption(plug_name, time, voltage, current, wph):
    """Ajoute des données de consommation d'énergie pour une prise."""
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO power_consumption (plug, time, voltage, current, wph)
        VALUES (%s, %s, %s, %s, %s)
    ''', (plug_name, time, voltage, current, wph))
    db.commit()
    db.close()
