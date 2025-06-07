# 🇫🇷 Jour Férié

Une intégration Home Assistant pour savoir si **aujourd’hui est un jour férié en France** .

---

## 📦 Fonctionnalités

- 🗓️ Capteur `sensor.jour_ferie` indiquant :
  - Le nom du jour férié, ou "Aucun"
  - Le prochain jour férié
  - Le nombre de jours restants
- 🧩 Configuration via l’interface graphique (UI)
- 🛠️ Service `jourferier.create_card` pour insérer automatiquement une carte Lovelace

---

## 🛠️ Installation

### Via HACS (recommandé)

1. Allez dans **HACS > Intégrations**
2. Cliquez sur les **trois points > Dépôt personnalisé**
3. Ajoutez ce dépôt :



Allez dans Paramètres > Appareils et services > Ajouter une intégration.



Recherchez "Jour Férié" et configurez-la.

Utilisation

Le capteur sensor.jour_ferie sera disponible après configuration. Vous pouvez l'ajouter à votre tableau de bord Lovelace avec une carte d'entité, par exemple :

type: entity
entity: sensor.jour_ferie
name: Jour Férié
icon: mdi:calendar-star

Service Lovelace

Pour ajouter automatiquement une carte dans la première vue de votre tableau de bord Lovelace, appelez le service suivant dans les outils de développement :

service: jourferier.create_card
