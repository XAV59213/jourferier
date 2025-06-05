"""Constantes pour le composant Jour Férié."""
DOMAIN = "jourferier"
SENSOR_NAME = "Jour Férié"
SENSOR_UNIQUE_ID = f"{DOMAIN}_sensor"
ATTR_HOLIDAY_NAME = "holiday_name"
ATTR_DATE = "date"

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