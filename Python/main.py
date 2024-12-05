from database import create_tables
from add_data import add_plug, add_scenario, add_power_consumption
from simulate import simulate_scenario

if __name__ == "__main__":
    # create_tables()  # Crée les tables nécessaires dans la base de données

    # Ajouter des prises
    # add_plug("Shelly0", 1)
    # add_plug("Shelly1", 2)
    # add_plug("Meross", 3)
    
    # Ajouter un scénario
    # add_scenario(100, 2, 70)  # Max 100W, 2 prises, 70% de couverture nuageuse
    # add_scenario(100, 3, 70)
    # add_scenario(100, 3, 20)
    # add_scenario(35, 3, 20)
    
    # Ajouter des données de consommation
    # add_power_consumption("Shelly0", "2024-12-03 15:51:59", 238.3, 0.2, 30.1)
    # add_power_consumption("Shelly1", "2024-12-03 15:51:59", 238.2, 0.185, 40.6)
    # add_power_consumption("Meross", "2024-12-03 15:52:00", 238.1, 0.211, 31.9)
    
    # Lancer la simulation pour le scénario avec ID 1
    simulate_scenario(2)
    simulate_scenario(3)
    simulate_scenario(4)
