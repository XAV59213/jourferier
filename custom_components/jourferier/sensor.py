"""Capteur pour afficher si aujourd'hui est un jour férié."""
import logging
from datetime import date, datetime, timedelta
from homeassistant.components.sensor import SensorEntity
from .const import (
    DOMAIN, SENSOR_NAME, SENSOR_UNIQUE_ID, PUBLIC_HOLIDAYS_2025 as HOLIDAYS,
    ATTR_HOLIDAY_NAME, ATTR_DATE, ATTR_NEXT_HOLIDAY, ATTR_DAYS_UNTIL
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([JourFerieSensor()])

class JourFerieSensor(SensorEntity):
    def __init__(self):
        self._attr_name = SENSOR_NAME
        self._attr_unique_id = SENSOR_UNIQUE_ID
        self._attr_icon = "mdi:calendar-star"
        self._state = None
        self._attributes = {}

    def update(self):
        """Met à jour le capteur pour le jour férié."""
        today = date.today()
        today_str = today.strftime("%d:%m")
        holiday = HOLIDAYS.get(today_str)
        self._state = holiday if holiday else "Aucun"

        # Calculer le prochain jour férié
        next_holiday = None
        days_until = None
        current_year = today.year

        # Convertir les dates des jours fériés en objets date pour l'année courante
        holiday_dates = []
        for date_str, name in HOLIDAYS.items():
            day, month = map(int, date_str.split(":"))
            holiday_date = date(current_year, month, day)
            holiday_dates.append((holiday_date, name))

        # Trier les dates et trouver la prochaine
        holiday_dates.sort()
        for holiday_date, name in holiday_dates:
            if holiday_date > today:
                next_holiday = name
                days_until = (holiday_date - today).days
                break

        # Si aucun jour férié n'est trouvé dans l'année courante, prendre le premier de l'année suivante
        if not next_holiday:
            first_holiday_date = date(current_year + 1, 1, 1)
            next_holiday = HOLIDAYS.get("01:01", "Jour de l’An")
            days_until = (first_holiday_date - today).days

        self._attributes = {
            ATTR_HOLIDAY_NAME: self._state,
            ATTR_DATE: today_str,
            ATTR_NEXT_HOLIDAY: next_holiday,
            ATTR_DAYS_UNTIL: days_until
        }

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes
