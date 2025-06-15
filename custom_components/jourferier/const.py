"""Constantes pour le composant Jour Férié."""
from datetime import date, timedelta

DOMAIN = "jourferier"
SENSOR_NAME = "Jour Férié"
SENSOR_UNIQUE_ID = f"{DOMAIN}_sensor"
ATTR_HOLIDAY_NAME = "holiday_name"
ATTR_DATE = "date"
ATTR_NEXT_HOLIDAY = "next_holiday"
ATTR_DAYS_UNTIL = "days_until"

def get_holidays(year: int) -> dict[date, str]:
    """Retourne un dictionnaire de dates de jours fériés pour l’année spécifiée."""
    # Calcul du dimanche de Pâques (méthode de Meeus/Jones/Butcher)
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    easter_sunday = date(year, month, day)

    return {
        date(year, 1, 1): "Jour de l’An",
        easter_sunday + timedelta(days=1): "Lundi de Pâques",
        date(year, 5, 1): "Fête du Travail",
        date(year, 5, 8): "Victoire 1945",
        easter_sunday + timedelta(days=39): "Ascension",
        easter_sunday + timedelta(days=50): "Lundi de Pentecôte",
        date(year, 7, 14): "Fête Nationale",
        date(year, 8, 15): "Assomption",
        date(year, 11, 1): "Toussaint",
        date(year, 11, 11): "Armistice 1918",
        date(year, 12, 25): "Noël"
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
