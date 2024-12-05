# États et priorités des prises
plugs = {
    "meross": {"state": False, "priority": 3, "topic": "/"},
    "shelly_switch_1": {"state": "off", "priority": 2, "topic": "Shelly-Solgaleo/status/switch:1"},
    "shelly_switch_0": {"state": "off", "priority": 1, "topic": "Shelly-Solgaleo/status/switch:0"},
}

# Fonction pour simuler le contrôle d'une prise
def control_plug(plug_name: str, state):
    """Simule le contrôle d'une prise en imprimant la commande MQTT."""
    if plug_name not in plugs:
        print(f"[Erreur] Prise inconnue : {plug_name}")
        return

    # Vérification de l'état actuel pour éviter les commandes inutiles
    if plugs[plug_name]["state"] == state:
        print(f"[Info] Aucun changement pour {plug_name}, déjà dans l'état demandé.")
        return

    topic = plugs[plug_name]["topic"]
    message = state if isinstance(state, str) else ("true" if state else "false")
    print(f"MQTT Commande : topic='{topic}', message='{message}'")
    plugs[plug_name]["state"] = state
    print(f"[{plug_name}] État modifié : {state}")

# Fonction principale : Gestion des priorités
def handle_priority():
    """Gère les prises en fonction de leur priorité."""
    print("Gestion des priorités des prises :")
    # Trier les prises par priorité croissante
    sorted_plugs = sorted(plugs.items(), key=lambda x: x[1]["priority"])

    # Allumer uniquement la prise de plus haute priorité
    highest_priority = sorted_plugs[0][1]["priority"]
    for plug_name, plug_info in sorted_plugs:
        if plug_info["priority"] == highest_priority:
            # Allumer la prise avec la plus haute priorité
            desired_state = "on" if isinstance(plug_info["state"], str) else True
            control_plug(plug_name, desired_state)
        else:
            # Éteindre les autres prises
            desired_state = "off" if isinstance(plug_info["state"], str) else False
            control_plug(plug_name, desired_state)

# Exemple d'utilisation
if __name__ == "__main__":
    # Initialisation : Afficher les états et priorités actuels
    print("État initial des prises et leurs priorités :")
    for plug, info in plugs.items():
        print(f"  - {plug}: État={info['state']}, Priorité={info['priority']}")

    # Gérer les prises en fonction des priorités
    handle_priority()

    # Afficher l'état final des prises
    print("État final des prises :")
    for plug, info in plugs.items():
        print(f"  - {plug}: État={info['state']}, Priorité={info['priority']}")
