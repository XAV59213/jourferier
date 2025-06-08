"""Constantes pour le composant Jour Férié."""
DOMAIN = "jourferier"
SENSOR_NAME = "Jour Férié"
SENSOR_UNIQUE_ID = f"{DOMAIN}_sensor"
ATTR_HOLIDAY_NAME = "holiday_name"
ATTR_DATE = "date"
ATTR_NEXT_HOLIDAY = "next_holiday"
ATTR_DAYS_UNTIL = "days_until"

PUBLIC_HOLIDAYS_2025 = {
    "01:01": "Jour de l’An",
    "21:04": "Lundi de Pâques",
    "01:05": "Fête du Travail",
    "08:05": "Victoire 1945",
    "29:05": "Ascension",
    "09:06": "Lundi de Pentecôte",
    "14:07": "Fête Nationale",
    "15:08": "Assomption",
    "01:11": "Toussaint",
    "11:11": "Armistice 1918",
    "25:12": "Noël"
}

HOLIDAY_DESCRIPTIONS = {
    "Jour de l’An": "Bonne année ! Que cette nouvelle année soit pleine de joie et de réussite !",
    "Lundi de Pâques": "Joyeuses Pâques ! Profitez de cette journée festive en famille !",
    "Fête du Travail": "Bonne fête du travail ! Une journée pour célébrer les travailleurs !",
    "Victoire 1945": "Hommage à la victoire de 1945 ! Une journée de mémoire et de paix.",
    "Ascension": "Joyeuse Ascension ! Une journée spirituelle et de repos.",
    "Lundi de Pentecôte": "Bonne fête de Pentecôte ! Une journée pour célébrer l'Esprit Saint.",
    "Fête Nationale": "Vive la France ! Joyeux 14 juillet, fête nationale !",
    "Assomption": "Bonne fête de l’Assomption ! Une journée de célébration mariale.",
    "Toussaint": "Bonne Toussaint ! Un moment pour honorer les saints et les défunts.",
    "Armistice 1918": "Hommage aux héros de 1918 ! Une journée de recueillement.",
    "Noël": "Joyeux Noël ! Une fête chaleureuse pour partager amour et cadeaux !"
}
