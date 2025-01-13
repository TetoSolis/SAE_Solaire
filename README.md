# Projet IoT - Gestion des Prises Connectées

## 📚 Introduction

Ce projet consiste à gérer des prises connectées via un système IoT, avec des fonctionnalités d'automatisation, de récupération des données et de surveillance de la consommation énergétique. Le système utilise XAMPP pour la base de données, Node-RED pour l'automatisation, et Mosquitto pour la gestion des messages MQTT.

***

## 🔧 Matériel Utilisé

### 1. Prises Connectées Shelly 🔌
Les prises Shelly permettent de contrôler la consommation d'énergie et de programmer leur fonctionnement à distance.

### 2. Prise Connectée Meross MSS310 ⚡
La prise Meross MSS310 est utilisée pour mesurer la consommation d'énergie des appareils connectés.

#### Obtention de la clé d'authentification 🔑
Pour l'intégration de la prise Meross, il est nécessaire de récupérer une clé d'authentification via l'API de Meross.

#### Intégration avec Node-RED 🌐
Les données des prises Meross sont envoyées à Node-RED via MQTT, ce qui permet de les utiliser dans des scénarios d'automatisation.

### 3. Raspberry Pi 🍓
Le projet est déployé sur un Raspberry Pi, qui sert de serveur pour exécuter Node-RED, Mosquitto et InfluxDB.

### 4. Infrastructure Logicielle 🖥️

#### Node-RED 🚦
Node-RED est utilisé pour créer des flux d'automatisation qui récupèrent les données des prises connectées et déclenchent des actions en fonction des scénarios définis.

#### Mosquitto 🐭
Mosquitto est un broker MQTT qui permet de gérer les communications entre les prises connectées et Node-RED.

#### InfluxDB 📊
InfluxDB est utilisé pour stocker les données de consommation énergétique des prises connectées, afin de pouvoir effectuer des analyses à long terme.

***

## 🔧 Installation

### 1. Installation de XAMPP 💻

1. Télécharge et installe XAMPP depuis [le site officiel](https://www.apachefriends.org/index.html).
2. Lance le serveur Apache et MySQL via le panneau de contrôle XAMPP.
3. Accède à `http://localhost/phpmyadmin` pour configurer ta base de données.

### 2. Utilisation de PHPMyAdmin 🗄️

1. Crée une nouvelle base de données nommée `solaire`.
2. Crée les tables suivantes dans la base de données :
   - **prise** : pour stocker les informations sur les prises connectées.
   - **scenarios** : pour gérer les scénarios d'automatisation.
   - **plugs** : pour associer les prises avec des éléments spécifiques.
   - **power_consumption** : pour enregistrer la consommation d'énergie.

### 3. Installation et Configuration de Node-RED 🌐

1. Installe Node-RED sur ton Raspberry Pi avec la commande suivante :
   ```
   sudo npm install -g --unsafe-perm node-red
   ```
2. Lance Node-RED avec la commande suivante :
   ```
   node-red
   ```
3. Accède à l'interface de Node-RED via `http://localhost:1880`.

### 4. Installation de Mosquitto 🐭

1. Installe Mosquitto sur ton Raspberry Pi avec :
   ```
   sudo apt install mosquitto mosquitto-clients
   ```
2. Lance Mosquitto pour le démarrer en tant que service :
   ```
   sudo systemctl start mosquitto
   ```

***

## 🧩 Automatisation avec Node-RED

Node-RED est utilisé pour automatiser les actions en fonction des données des prises connectées. Voici les étapes principales :

1. **Récupération des Données** : Node-RED interagit avec les prises connectées via MQTT pour récupérer les données de consommation.
2. **Automatisation Basée sur les Données Météorologiques** : Des scénarios peuvent être déclenchés en fonction de la météo ou d'autres paramètres externes.
3. **Interface Graphique avec Node-RED Dashboard** : Un tableau de bord est créé pour visualiser la consommation d'énergie en temps réel.

***

## 📊 Base de Données MySQL

### Structure de la Base de Données

- **Table `prise`** : Contient les informations des prises connectées.
- **Table `scenarios`** : Gère les différents scénarios d'automatisation.
- **Table `plugs`** : Associe les prises aux différents éléments à contrôler.
- **Table `power_consumption`** : Enregistre la consommation énergétique des prises connectées.

### Interaction avec les Prises Connectées

Les données des prises connectées sont collectées et enregistrées dans la base de données pour un suivi en temps réel de leur consommation d'énergie.

***

## 🐍 Script Python

Le script Python collecte les données des prises connectées, les enregistre dans la base de données MySQL et supervise les scénarios énergétiques.

### Fonctionnalités du Script

1. **Collecte des Données** : Le script récupère périodiquement les données de consommation des prises connectées.
2. **Enregistrement des Données** : Les données sont enregistrées dans la base de données MySQL.
3. **Supervision des Scénarios** : Le script évalue les scénarios énergétiques et ajuste les priorités en fonction des paramètres définis.
4. **Détection des Anomalies** : Des alertes sont créées si des anomalies de consommation sont détectées.

***

## 📦 Contributeurs

Ce projet a été réalisé par :

- **Guillaume Greder** : Développement de la solution IoT et gestion de la base de données.
- **Théo Marchand** : Intégration des prises connectées et gestion de l'automatisation avec Node-RED.
- **Xavier Knoeppfler** : Configuration de l'infrastructure logicielle et gestion du serveur.

***

## 🚀 Perspectives

Ce projet peut être amélioré en ajoutant :

- L'intégration de nouvelles prises connectées.
- Des améliorations de l'interface utilisateur de Node-RED.
- Des options d'optimisation énergétique plus avancées basées sur l'IA.

Merci d'avoir exploré ce projet ! N'hésitez pas à contribuer ou à poser des questions.
