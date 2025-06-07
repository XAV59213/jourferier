our Férié

Une intégration Home Assistant qui affiche si aujourd'hui est un jour férié (France 2025).

Fonctionnalités





Capteur sensor.jour_ferie avec le nom du jour férié ou "Aucun".



Service jourferier.create_card pour insérer une carte dans le tableau de bord Lovelace.



Configuration via l'interface utilisateur (UI).

Installation





Ajoutez ce dépôt comme dépôt personnalisé dans HACS.



Installez l'intégration Jour Férié.



Redémarrez Home Assistant.



Ajoutez l'intégration via l'interface utilisateur :





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
