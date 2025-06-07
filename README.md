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
https://github.com/xav59213/xav59213-jour-ferie

(type : Intégration)
4. Installez **Jour Férié**
5. Redémarrez Home Assistant
6. Allez dans **Paramètres > Appareils & Services > Ajouter une intégration**
7. Recherchez **Jour Férié** et suivez les instructions

---

## 📊 Exemple de carte Lovelace

```yaml
type: entity
entity: sensor.jour_ferie
name: Jour Férié
icon: mdi:calendar-star

🧩 Service Lovelace

Ajoutez une carte automatiquement en appelant ce service depuis les outils de développement :

service: jourferier.create_card

🔍 Capteur : sensor.jour_ferie
Attribut	Description
state	Nom du jour férié ou "Aucun"
holiday_name	Nom du jour férié
date	Date du jour (format DD:MM)
next_holiday	Prochain jour férié
days_until	Nombre de jours restants
📅 Jours fériés inclus (2025)

    Jour de l’An – 1er janvier

    Lundi de Pâques – 21 avril

    Fête du Travail – 1er mai

    Victoire 1945 – 8 mai

    Ascension – 29 mai

    Lundi de Pentecôte – 9 juin

    Fête Nationale – 14 juillet

    Assomption – 15 août

    Toussaint – 1er novembre

    Armistice 1918 – 11 novembre

    Noël – 25 décembre

🔧 Infos techniques

    Domaine : jourferier

    Configuration : UI (config_flow)

    Code propriétaire : @xav59213

    📂 Code source

    🐞 Bug tracker

    🇫🇷 Un petit composant simple et pratique pour rester informé des jours fériés en France !


---

### 📢 Présentation pour forum (Home Assistant, Domotique, etc.)

---

## 🇫🇷 [Intégration HA] Jour Férié – Capteur de jours fériés (France 2025)

Salut à tous ! 👋

Voici une intégration que j’ai développée pour Home Assistant : **Jour Férié**.

### 🗓️ Description

Cette intégration vous permet d’afficher dans votre interface si **aujourd’hui est un jour férié en France**, et vous indique également **le prochain jour férié** avec le nombre de jours restants.

### ✅ Fonctionnalités

- `sensor.jour_ferie` ➜ indique le jour férié actuel (ou "Aucun")
- Attributs disponibles :
  - `holiday_name`, `date`, `next_holiday`, `days_until`
- Service `jourferier.create_card` ➜ ajoute automatiquement une carte dans Lovelace
- Intégration complète via l'interface utilisateur (aucun YAML requis)

---

### 🔧 Installation via HACS

1. Dans **HACS > Intégrations**, ajoutez ce dépôt :

https://github.com/xav59213/xav59213-jour-ferie

2. Installez **Jour Férié**
3. Redémarrez Home Assistant
4. Allez dans **Paramètres > Appareils et Services > Ajouter une intégration**
5. Recherchez **Jour Férié**

---

### 🧾 Exemple de carte Lovelace

```yaml
type: entity
entity: sensor.jour_ferie
name: Jour Férié
icon: mdi:calendar-star

🔨 Service disponible

Pour ajouter automatiquement une carte :

service: jourferier.create_card

À appeler via les outils de développement ou une automatisation.
💡 Infos utiles

    Domaine : jourferier

    Année supportée : 2025

    Fonctionne localement (pas d’appel API)

    Compatible HA >= 2024.6.0

🗨️ Questions, suggestions ou bugs ➜ page GitHub

Bonne domotique à tous ! 🤖
— xav59213
