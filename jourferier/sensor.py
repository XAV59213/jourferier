"""Capteur pour afficher si aujourd'hui est un jour férié.""" 
import logging
from datetime import date
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN, SENSOR_NAME, SENSOR_UNIQUE_ID, HOLIDAYS, ATTR_HOLIDAY_NAME, ATTR_DATE

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
        today = date.today().strftime("%d:%m")
        holiday = HOLIDAYS.get(today)
        self._state = holiday if holiday else "Aucun"
        self._attributes = {
            ATTR_HOLIDAY_NAME: self._state,
            ATTR_DATE: today
        }

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes
