"""Capteur pour afficher si aujourd'hui est un jour férié."""
import logging
from datetime import date
from homeassistant.components.sensor import SensorEntity
from .const import (
    SENSOR_NAME, SENSOR_UNIQUE_ID,
    ATTR_HOLIDAY_NAME, ATTR_DATE, ATTR_NEXT_HOLIDAY, ATTR_DAYS_UNTIL,
    ATTR_PROCHAIN_PONT_POTENTIEL, get_device_info, get_holidays,
    get_next_potential_bridge, holiday_settings_from_entry,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([JourFerieSensor(entry)])

class JourFerieSensor(SensorEntity):
    def __init__(self, entry):
        self._entry = entry
        self._attr_name = SENSOR_NAME
        self._attr_unique_id = SENSOR_UNIQUE_ID
        self._attr_icon = "mdi:calendar-star"
        self._state = None
        self._attributes = {}
        self._attr_device_info = get_device_info()

    def update(self):
        today = date.today()
        settings = holiday_settings_from_entry(self._entry)
        holidays = get_holidays(today.year, **settings)
        today_holiday = holidays.get(today)
        self._state = today_holiday if today_holiday else "aucun"

        # Inclure aussi l'année suivante pour calcul anticipé
        all_holidays = {**holidays, **get_holidays(today.year + 1, **settings)}
        next_holiday = None
        days_until = None
        for holiday_date in sorted(all_holidays):
            if holiday_date > today:
                next_holiday = all_holidays[holiday_date]
                days_until = (holiday_date - today).days
                break

        next_potential_bridge = get_next_potential_bridge(today, **settings)

        self._attributes = {
            ATTR_HOLIDAY_NAME: self._state,
            ATTR_DATE: today.strftime("%d:%m"),
            ATTR_NEXT_HOLIDAY: next_holiday,
            ATTR_DAYS_UNTIL: days_until,
            ATTR_PROCHAIN_PONT_POTENTIEL: (
                next_potential_bridge.strftime("%d:%m")
                if next_potential_bridge
                else "aucun"
            ),
        }

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes
