# 🇫🇷 Jour Férié

Une intégration Home Assistant pour savoir si **aujourd’hui est un jour férié en France** et afficher les jours fériés dans le calendrier Home Assistant.

<a href="https://www.buymeacoffee.com/xav59213"> <img src="https://img.buymeacoffee.com/button-api/?text=xav59213&emoji=&slug=xav59213&button_colour=5F7FFF&font_colour=ffffff&font_family=Cookie&outline_colour=000000&coffee_colour=FFDD00" /> </a>

---

## 📦 Fonctionnalités

- 🗓️ **Capteur** `sensor.jour_ferie` indiquant :
  - Le nom du jour férié, ou "Aucun"
  - Le prochain jour férié
  - Le nombre de jours restants
- 📅 **Calendrier** `calendar.jour_ferie_calendar` affichant les jours fériés de 2025 comme des événements d'une journée entière.
- 🧩 Configuration via l’interface graphique (UI)
- 🛠️ Service `jourferier.create_card` pour insérer automatiquement une carte Lovelace

---

## 🛠️ Installation

### Via HACS (recommandé)

1. Allez dans **HACS > Intégrations**
2. Cliquez sur les **trois points > Dépôt personnalisé**
3. Ajoutez ce dépôt : `https://github.com/xav59213/xav59213-jour-ferie` (type : Intégration)
4. Installez **Jour Férié**
5. Redémarrez Home Assistant
6. Allez dans **Paramètres > Appareils & Services > Ajouter une intégration**
7. Recherchez **Jour Férié** et suivez les instructions

---

## 📊 Utilisation

### Capteur
Le capteur `sensor.jour_ferie` sera disponible après configuration. Vous pouvez l'ajouter à votre tableau de bord Lovelace avec une carte d'entité, par exemple :

```yaml
type: entity
entity: sensor.jour_ferie
name: Jour Férié
icon: mdi:calendar-star
