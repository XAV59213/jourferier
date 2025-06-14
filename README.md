🇫🇷 Jour Férié
Une intégration Home Assistant pour suivre les jours fériés en France. Affichez si aujourd’hui est un jour férié via un capteur et intégrez les jours fériés de 2025 dans votre calendrier Home Assistant.


  



📦 Fonctionnalités

🗓️ Capteur sensor.jour_ferie : Affiche les informations suivantes :
Nom du jour férié actuel (ou "Aucun" si ce n’est pas un jour férié).
Prochain jour férié à venir.
Nombre de jours restants jusqu’au prochain jour férié.


📅 Calendrier calendar.jour_ferie_calendar : Intègre les jours fériés de 2025 comme des événements d’une journée entière, avec descriptions.
🧩 Configuration simple : Installation et configuration via l’interface graphique (UI).
🛠️ Service jourferier.create_card : Ajoute automatiquement une carte Lovelace pour afficher le capteur.


🛠️ Installation
Prérequis

Home Assistant version 2024.6.0 ou supérieure.
HACS (recommandé pour une installation simplifiée).

Installation via HACS (recommandé)

Ouvrez HACS dans Home Assistant (HACS > Intégrations).
Cliquez sur les trois points en haut à droite, puis sélectionnez Dépôt personnalisé.
Ajoutez le dépôt :  https://github.com/xav59213/xav59213-jour-ferie

Type : Intégration.
Recherchez et installez Jour Férié.
Redémarrez Home Assistant.
Allez dans Paramètres > Appareils & Services > Ajouter une intégration.
Recherchez Jour Férié et configurez l’intégration (aucun paramètre requis).

Installation manuelle

Téléchargez la dernière version du dépôt depuis GitHub.
Copiez le dossier custom_components/jourferier dans /config/custom_components/ de votre installation Home Assistant.
Redémarrez Home Assistant.
Ajoutez l’intégration via Paramètres > Appareils & Services > Ajouter une intégration > Jour Férié.


📊 Utilisation
Capteur : sensor.jour_ferie
Affichez les informations sur les jours fériés dans une carte Lovelace.
Exemple de carte d’entité
type: entity
entity: sensor.jour_ferie
name: Jour Férié
icon: mdi:calendar-star

Exemple de carte Markdown avec template
Affichez des informations personnalisées sur le jour férié actuel et le prochain :
type: markdown
content: |
  {% set sensor = 'sensor.jour_ferie' %}
  {% set holiday_name = state_attr(sensor, 'holiday_name') | default('Aucun') %}
  {% set today_holiday = holiday_name if holiday_name != 'Aucun' else None %}
  {% set next_holiday = state_attr(sensor, 'next_holiday') | default(None) %}
  {% set days_until = state_attr(sensor, 'days_until') | default(None) %}
  {% if today_holiday %}
  - 🎉 **Aujourd'hui, c'est {{ today_holiday }} !**
  {% else %}
  - Aujourd'hui, pas de jour férié.
  {% endif %}
  {% if next_holiday and days_until is not none and days_until | float >= 0 %}
  - Le prochain jour férié est **{{ next_holiday }}** dans **{{ days_until | int }} jour{{ 's' if days_until | int != 1 else '' }}**.
  {% else %}
  - Aucun jour férié à venir. Vérifiez la configuration du capteur {{ sensor }}.
  {% endif %}


Calendrier : calendar.jour_ferie_calendar
Affichez les jours fériés de 2025 dans une carte de calendrier.
Exemple de carte de calendrier
type: calendar
entities:
  - calendar.jour_ferie_calendar


Service Lovelace : jourferier.create_card
Ajoutez automatiquement une carte pour sensor.jour_ferie dans la première vue de votre tableau de bord :

Ouvrez Outils de développement > Services.
Sélectionnez le service jourferier.create_card.
Appelez le service (aucun paramètre requis).

Exemple YAML pour une automatisation :
service: jourferier.create_card


🔍 Détails du capteur : sensor.jour_ferie



Attribut
Description



state
Nom du jour férié ou "Aucun"


holiday_name
Nom du jour férié actuel


date
Date du jour (format DD:MM)


next_holiday
Nom du prochain jour férié


days_until
Nombre de jours jusqu’au prochain jour férié



📅 Jours fériés inclus (2025)



Date
Jour férié



1er janvier
Jour de l’An


21 avril
Lundi de Pâques


1er mai
Fête du Travail


8 mai
Victoire 1945


29 mai
Ascension


9 juin
Lundi de Pentecôte


14 juillet
Fête Nationale


15 août
Assomption


1er novembre
Toussaint


11 novembre
Armistice 1918


25 décembre
Noël



🔧 Infos techniques

Domaine : jourferier
Configuration : Via l’interface graphique (config_flow)
Propriétaire : @xav59213
Code source : GitHub
Suivi des bugs : Issues
Version : 1.0.5
Compatibilité : Home Assistant 2024.6.0 ou supérieur
Dépendances : Aucune


🛠️ Résolution des problèmes
L’entité calendar.jour_ferie_calendar n’apparaît pas

Vérifiez les logs :docker logs <votre_conteneur>

Ou consultez Paramètres > Système > Journaux.Recherchez des erreurs liées à jourferier ou calendar.
Activez le débogage :Ajoutez à configuration.yaml :logger:
  default: info
  logs:
    custom_components.jourferier: debug
    homeassistant.components.calendar: debug

Redémarrez et consultez les logs.
Vérifiez la version de Home Assistant :Assurez-vous d’utiliser une version ≥ 2024.6.0 (Paramètres > Système > Informations).
Réinstallez l’intégration :
Supprimez /config/custom_components/jourferier.
Supprimez l’intégration via Paramètres > Appareils & Services.
Réinstallez via HACS ou manuellement.
Redémarrez et reconfigurez.



Erreur de template avec sensor.jour_ferie
Si vous rencontrez des erreurs comme TypeError: logarithm() got an unexpected keyword argument 'level' :

Localisez le template dans une carte Lovelace, une automatisation, ou configuration.yaml.
Utilisez le template corrigé fourni ci-dessus.
Ajoutez une automatisation pour journaliser les erreurs si nécessaire :- id: log_jour_ferie_status
  alias: Journaliser l'état du jour férié
  trigger:
    - platform: state
      entity_id: sensor.jour_ferie
  condition:
    - condition: template
      value_template: "{{ state_attr('sensor.jour_ferie', 'next_holiday') is none or state_attr('sensor.jour_ferie', 'days_until') is none }}"
  action:
    - service: system_log.write
      data:
        message: "Invalid or missing attributes for sensor.jour_ferie: next_holiday={{ state_attr('sensor.jour_ferie', 'next_holiday') }}, days_until={{ state_attr('sensor.jour_ferie', 'days_until') }}"
        level: warning




🙌 Contribuer

Signaler un bug : Ouvrez une issue sur GitHub.
Proposer une amélioration : Soumettez une pull request ou partagez vos idées.
Soutenir le projet : Offrez un café via Buy Me a Coffee.

🇫🇷 Un composant simple, pratique et festif pour ne jamais rater un jour férié en France !

