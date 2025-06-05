# Jour Férié

Une intégration Home Assistant qui affiche si aujourd'hui est un jour férié (France 2025).

## Fonctionnalités

- Capteur `sensor.jour_ferie` avec le nom du jour férié ou "Aucun".
- Service `jourferier.create_card` pour insérer une carte dans le tableau de bord Lovelace.
- Intégration UI (`config_flow`) via HACS.

## Installation

1. Ajoutez ce dépôt comme dépôt personnalisé dans HACS.
2. Installez l'intégration `Jour Férié`.
3. Redémarrez Home Assistant.
4. Ajoutez l'intégration via **Paramètres > Appareils & Services**.

## Service Lovelace

Vous pouvez appeler le service dans les outils de développement :

```yaml
service: jourferier.create_card
```

Cela ajoutera automatiquement une carte de type `sensor` dans la première vue Lovelace.
