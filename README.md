
# 🇫🇷 Jour Férié

# 📨 Jour Férié – Intégration Home Assistant

![Logo](https://raw.githubusercontent.com/XAV59213/jourferier/main/image/logo.png)

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz) [![Release](https://img.shields.io/github/v/release/XAV59213/jourferier?label=release)](https://github.com/XAV59213/jourferier/releases/latest) [![Hassfest](https://img.shields.io/github/actions/workflow/status/XAV59213/jourferier/hassfest.yaml?branch=main&label=Hassfest&logo=github)](https://github.com/XAV59213/jourferier/actions/workflows/hassfest.yaml) [![HACS validation](https://img.shields.io/github/actions/workflow/status/XAV59213/jourferier/validate.yaml?branch=main&label=HACS%20validation&logo=github)](https://github.com/XAV59213/jourferier/actions/workflows/validate.yaml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Downloads](https://img.shields.io/github/downloads/XAV59213/jourferier/total.svg?label=Downloads)](https://github.com/XAV59213/jourferier/releases) [![Version](https://img.shields.io/github/v/release/XAV59213/jourferier?label=VERSION&color=blue)](https://github.com/XAV59213/jourferier/releases/latest) [![Home Assistant](https://img.shields.io/badge/HOME%20ASSISTANT-%3E%3D2024.6.0-41BDF5.svg)](https://www.home-assistant.io)

[![Buy Me A Coffee](https://img.buymeacoffee.com/button-api/?text=xav59213&emoji=&slug=xav59213&button_colour=5F7FFF&font_colour=ffffff&font_family=Cookie&outline_colour=000000&coffee_colour=FFDD00)](https://www.buymeacoffee.com/xav59213)

## Via HACS (recommandé)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=XAV59213&repository=jourferier&category=integration)

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=jourferier)


**Une intégration Home Assistant pour suivre les jours fériés en France**  
Affichez si **aujourd’hui ou demain est un jour férié** via des capteurs et **intégrez automatiquement les jours fériés** dans votre calendrier Home Assistant.

---

## 📦 Fonctionnalités

- 🗓️ **Capteur `sensor.jour_ferie`**
  - Nom du jour férié actuel (ou `Aucun`)
  - Prochain jour férié
  - Nombre de jours restants
  - Date du prochain pont potentiel

- 🔀 **Binary sensor `binary_sensor.est_ferie`**
  - `on` = Aujourd’hui est un jour férié
  - `off` = Jour normal
  - Attributs `holiday_name` et `date`
  - **Idéal pour bloquer réveils, alarmes, etc.**

- 🔀 **Binary sensor `binary_sensor.demain_est_ferie`**
  - `on` = Demain est un jour férié
  - `off` = Demain est un jour normal
  - Attributs `holiday_name` et `date` du lendemain
  - Utile pour préparer la veille (réveil, chauffage, poubelles…)

- 📅 **Calendrier `calendar.jour_ferie_calendar`**
  - Événements sur une journée complète pour chaque jour férié 

- 🧩 **Configuration simplifiée**
  - Ajout via l’interface Home Assistant (UI)

---

## 🛠️ Installation

### ✅ Prérequis

- Home Assistant ≥ `2024.6.0`
- [HACS](https://hacs.xyz/) recommandé

### 📥 Installation via HACS (recommandée)

1. Ouvrir **HACS > Intégrations**
2. Cliquer sur ⋮ > **Dépôt personnalisé**
3. Ajouter ce dépôt :
   ```
   https://github.com/XAV59213/jourferier
   ```
   Type : **Intégration**
4. Rechercher et installer **Jour Férié**
5. Redémarrer Home Assistant
6. Aller dans **Paramètres > Appareils & Services > Ajouter une intégration**
7. Sélectionner **Jour Férié** (aucune configuration requise)

### 📂 Installation manuelle

1. Télécharger la dernière version du dépôt
2. Copier le dossier `custom_components/jourferier` vers :
   ```
   /config/custom_components/
   ```
3. Redémarrer Home Assistant
4. Ajouter l’intégration via **Paramètres > Appareils & Services**

---

## 📊 Utilisation

### 🔎 Capteur : `sensor.jour_ferie`

#### 📋 Exemple carte d'entité

```yaml
type: entity
entity: sensor.jour_ferie
name: Jour Férié
icon: mdi:calendar-star
```

#### 📝 Exemple carte Markdown (template)

```yaml
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
```

---

### 🗓️ Calendrier : `calendar.jour_ferie_calendar`

#### Exemple carte calendrier :

```yaml
type: calendar
entities:
  - calendar.jour_ferie_calendar
```
### 🔀 Binary sensors

#### Aujourd'hui : `binary_sensor.est_ferie`

```yaml
# Condition pour bloquer un réveil les jours fériés
condition:
  - condition: state
    entity_id: binary_sensor.est_ferie
    state: "off"
```

#### Demain : `binary_sensor.demain_est_ferie`

```yaml
# La veille d'un jour férié
condition:
  - condition: state
    entity_id: binary_sensor.demain_est_ferie
    state: "on"
```
---

### 🎉 Carte Lovelace native : « Jours fériés »

L'intégration fournit sa propre carte (`custom:jour-ferie-card`), aucune installation séparée :
la ressource `/jourferier/jour-ferie-card.js` est servie et ajoutée automatiquement aux ressources Lovelace.

- Tableau de bord → **Modifier** → **Ajouter une carte** → **Jours fériés**
- Éditeur visuel : choix du capteur (`sensor.jour_ferie` par défaut) et du titre

Rendu : « Aujourd'hui, pas de jour férié. » (ou « Aujourd'hui, c'est **Noël**. ») puis
« Le prochain jour férié est **Toussaint** dans **1 jour**. »

```yaml
type: custom:jour-ferie-card
entity: sensor.jour_ferie
title: Jours fériés 🎉
```

Si la carte n'apparaît pas : vider le cache du navigateur, ou ajouter à la main
`/jourferier/jour-ferie-card.js` en **module JavaScript** (Paramètres → Tableaux de bord → Ressources).

---

## 🔍 Détails du capteur

| Attribut       | Description                                 |
|----------------|---------------------------------------------|
| `state`        | Nom du jour férié ou `Aucun`                |
| `holiday_name` | Nom du jour férié actuel                    |
| `date`         | Date du jour (format `DD:MM`)               |
| `next_holiday` | Nom du prochain jour férié                  |
| `days_until`   | Nombre de jours restants jusqu’au prochain |
| `prochain_pont_potentiel` | Date (`DD:MM`) du prochain jour ouvré entre deux jours de repos (week-end ou jour férié), ou `Aucun` |

---

## 📅 Jours fériés inclus

| Date         | Jour férié             |
|--------------|------------------------|
| 1er janvier  | Jour de l’An           |
| Lundi de Pâques | Lundi de Pâques     |
| 1er mai      | Fête du Travail        |
| 8 mai        | Victoire 1945          |
| Ascension    | Ascension              |
| Lundi de Pentecôte | Lundi de Pentecôte |
| 14 juillet   | Fête Nationale         |
| 15 août      | Assomption             |
| 1er novembre | Toussaint              |
| 11 novembre  | Armistice 1918         |
| 25 décembre  | Noël                   |

---

## ⚙️ Informations techniques

| Élément          | Détail                             |
|------------------|------------------------------------|
| **Domaine**       | `jourferier`                      |
| **Configuration** | Interface graphique (`config_flow`) |
| **Propriétaire**  | [@XAV59213](https://github.com/XAV59213) |
| **Code source**   | [GitHub](https://github.com/XAV59213/jourferier) |
| **Suivi bugs**    | [Issues](https://github.com/XAV59213/jourferier/issues) |
| **Version**       | `1.2.7`                            |
| **Compatibilité** | Home Assistant ≥ `2024.6.0`       |
| **Dépendances**   | Aucune                             |

---

## 🙌 Contribuer

- 🐞 **Signaler un bug** : [Créer une issue](https://github.com/XAV59213/jourferier/issues)
- 💡 **Proposer une amélioration** : Pull Request bienvenue !
- ☕ **Soutenir le projet** : [Buy Me a Coffee](https://www.buymeacoffee.com/xav59213) 

---

> 🇫🇷 **Un composant simple, pratique et festif pour ne jamais rater un jour férié en France !**
