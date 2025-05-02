# Documentation du Projet BlockSecure

## 1. Description du Projet

BlockSecure est une application web prototype conçue pour la surveillance et l'analyse en temps réel (ou simulée) des transactions blockchain. Elle vise à répondre aux besoins croissants de transparence et de détection de fraudes dans l'écosystème des cryptomonnaies.

L'application permet de :
- Stocker les données de transactions blockchain dans une base de données NoSQL (MongoDB).
- Visualiser ces transactions via un tableau de bord web interactif.
- Détecter automatiquement les transactions potentiellement suspectes grâce à un moteur d'analyse simple.
- Générer des alertes pour les transactions identifiées comme suspectes.

## 2. Technologies Utilisées

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **Base de données:** MongoDB (NoSQL, orientée documents)
- **Bibliothèques Python Principales:**
    - `pymongo`: Pour l'interaction avec MongoDB.
    - `flask`: Micro-framework web.
    - `bson.json_util`: Pour la sérialisation des types de données MongoDB.
- **Environnement:** Python 3.11, Ubuntu 22.04

## 3. Architecture Simplifiée

L'application suit une architecture web classique :

```
+-----------------+      +---------------------+      +-----------------------+      +-----------------+
| Utilisateur     | ---> | Interface Web (HTML)| ---> | Backend (Flask API)   | ---> | Base MongoDB    |
| (Analyste/Admin)|      | (templates/index.html)|      | (src/main.py)         |      | (blocksecure_db)|
+-----------------+      +---------------------+      +-----------+-----------+      +-----------------+
                                                            |
                                                            v
                                                      +-----------------------+
                                                      | Moteur d'Analyse      |
                                                      | (src/analysis.py)     |
                                                      +-----------------------+
```

1.  **Interface Web:** Fournit le tableau de bord à l'utilisateur. Elle communique avec le backend via des appels API (fetch).
2.  **Backend (Flask API):** Sert l'interface web et expose des points de terminaison (endpoints) API pour :
    - Récupérer les transactions (`/api/transactions`).
    - Déclencher l'analyse des anomalies (`/api/analyze`).
3.  **Moteur d'Analyse:** Contient la logique pour identifier les transactions suspectes. Actuellement, il implémente une règle simple basée sur un seuil de montant.
4.  **Base MongoDB:** Stocke les données des transactions dans la collection `transactions` de la base `blocksecure_db`.

## 4. Structure du Projet

```
/home/ubuntu/
|-- blocksecure_app/
|   |-- src/
|   |   |-- main.py       # Fichier principal de l'application Flask (API)
|   |   |-- analysis.py   # Module de détection d'anomalies
|   |-- templates/
|   |   |-- index.html    # Fichier HTML du tableau de bord
|-- setup_db.py           # Script pour initialiser la base de données MongoDB
|-- requirements.txt      # Dépendances Python
|-- todo.md               # Suivi des tâches
|-- project_description.txt # Texte extrait du PDF original
|-- README.md             # Ce fichier
|-- ANOMALY_DETECTION.md  # Explication de l'algorithme
|-- QUESTIONS_REPONSES.md # Réponses aux questions du PDF
```

## 5. Installation et Exécution

1.  **Prérequis:**
    - MongoDB installé et démarré (`sudo systemctl start mongod`).
    - Python 3.11 et pip.
2.  **Installer les dépendances Python:**
    ```bash
    cd /home/ubuntu
    python3.11 -m pip install -r requirements.txt
    ```
3.  **Initialiser la base de données (si nécessaire):**
    ```bash
    python3.11 setup_db.py
    ```
4.  **Lancer l'application Flask:**
    ```bash
    cd /home/ubuntu/blocksecure_app/src
    python3.11 main.py
    ```
5.  **Accéder à l'application:** Ouvrir un navigateur et aller à `http://<votre_ip>:5000` (ou `http://127.0.0.1:5000` si exécuté localement).

## 6. Fonctionnalités

- **Affichage des Transactions:** Le tableau de bord affiche les transactions récupérées depuis MongoDB.
- **Détection d'Anomalies:** Cliquer sur le bouton "Analyser les Transactions" déclenche le script `analysis.py`.
- **Mise en Évidence:** Les transactions identifiées comme suspectes sont mises en évidence en rouge dans le tableau.
- **Alertes:** Une section d'alerte liste les transactions suspectes détectées.
- **Rafraîchissement Automatique:** Après l'analyse, la liste des transactions est automatiquement rafraîchie pour montrer les mises à jour (statut suspect et notes).

