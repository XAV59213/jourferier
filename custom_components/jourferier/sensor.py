"""Capteur pour afficher si aujourd'hui est un jour férié."""
import logging
from datetime import date
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

        # ✅ Appareil visible dans "Appareils & Services"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, "jourferier")},
            "name": "Jour Férié",
            "manufacturer": "xav59213",
            "model": "Capteur jours fériés 2025",
            "sw_version": "1.0.6",
            "configuration_url": "https://github.com/xav59213/xav59213-jour-ferie",
        }

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

        holiday_dates = []
        for date_str, name in HOLIDAYS.items():
            day, month = map(int, date_str.split(":"))
            holiday_date = date(current_year, month, day)
            holiday_dates.append((holiday_date, name))

        holiday_dates.sort()
        for holiday_date, name in holiday_dates:
            if holiday_date > today:
                next_holiday = name
                days_until = (holiday_date - today).days
                break

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
