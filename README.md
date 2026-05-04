
# 🇫🇷 Jour Férié

# 📨 Jour Férié – Intégration Home Assistant

![Logo](./image/logo.png)

[![GitHub release](https://img.shields.io/github/v/release/XAV59213/jourferier)](https://github.com/XAV59213/jourferier/releases)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg?logo=home-assistant)](https://hacs.xyz/)
[![License: LGPL v2.1](https://img.shields.io/badge/License-LGPL%20v2.1-blue.svg)](./LICENSE)

**Une intégration Home Assistant pour suivre les jours fériés en France**  
Affichez si **aujourd’hui est un jour férié** via un capteur et **intégrez automatiquement les jours fériés** dans votre calendrier Home Assistant.

<a href="https://www.buymeacoffee.com/xav59213"> <img src="https://img.buymeacoffee.com/button-api/?text=xav59213&emoji=&slug=xav59213&button_colour=5F7FFF&font_colour=ffffff&font_family=Cookie&outline_colour=000000&coffee_colour=FFDD00" /> </a>
---

## 📦 Fonctionnalités

- 🗓️ **Capteur `sensor.jour_ferie`**
  - Nom du jour férié actuel (ou `Aucun`)
  - Prochain jour férié
  - Nombre de jours restants

- 🔀 **Binary sensor `binary_sensor.est_ferie`** *(nouveau)*
  - `on` = Aujourd’hui est un jour férié
  - `off` = Jour normal
  - Attribut `holiday_name` si férié
  - **Idéal pour bloquer réveils, alarmes, etc.**

- 📅 **Calendrier `calendar.jour_ferie_calendar`**
  - Événements sur une journée complète pour chaque jour férié 

- 🧩 **Configuration simplifiée**
  - Ajout via l’interface Home Assistant (UI)

- 🛠️ **Service `jourferier.create_card`**
  - Ajoute automatiquement une carte Lovelace pour le capteur
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
   https://github.com/xav59213/jourferier
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

---

### 🛠️ Service Lovelace : `jourferier.create_card`

Ajoute automatiquement une carte pour `sensor.jour_ferie` dans la première vue Lovelace.

#### Exécution manuelle :
- Aller dans **Outils de développement > Services**
- Choisir : `jourferier.create_card`
- Appeler le service (sans paramètres)

#### Exemple YAML pour automatisation :

```yaml
service: jourferier.create_card
```

---

## 🔍 Détails du capteur

| Attribut       | Description                                 |
|----------------|---------------------------------------------|
| `state`        | Nom du jour férié ou `Aucun`                |
| `holiday_name` | Nom du jour férié actuel                    |
| `date`         | Date du jour (format `DD:MM`)               |
| `next_holiday` | Nom du prochain jour férié                  |
| `days_until`   | Nombre de jours restants jusqu’au prochain |

---

## 📅 Jours fériés inclus (2025)

| Date         | Jour férié             |
|--------------|------------------------|
| 1er janvier  | Jour de l’An           |
| 21 avril     | Lundi de Pâques        |
| 1er mai      | Fête du Travail        |
| 8 mai        | Victoire 1945          |
| 29 mai       | Ascension              |
| 9 juin       | Lundi de Pentecôte     |
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
| **Propriétaire**  | [@xav59213](https://github.com/xav59213) |
| **Code source**   | [GitHub](https://github.com/xav59213/jourferier) |
| **Suivi bugs**    | [Issues](https://github.com/xav59213/jourferier/issues) |
| **Version**       | `1.0.5`                            |
| **Compatibilité** | Home Assistant ≥ `2024.6.0`       |
| **Dépendances**   | Aucune                             |

---



## 🙌 Contribuer

- 🐞 **Signaler un bug** : [Créer une issue](https://github.com/xav59213/jourferier/issues)
- 💡 **Proposer une amélioration** : Pull Request bienvenue !
- ☕ **Soutenir le projet** : [Buy Me a Coffee]([https://www.buymeacoffee.com/](https://www.buymeacoffee.com/xav59213)) 

---

> 🇫🇷 **Un composant simple, pratique et festif pour ne jamais rater un jour férié en France !**
