"""Binary sensor pour indiquer si aujourd'hui est un jour férié."""
import logging
from datetime import timedelta
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.util import dt as dt_util
from .const import DOMAIN, get_holidays, ATTR_HOLIDAY_NAME, ATTR_DATE, VERSION, MANUFACTURER

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Configurer la plateforme binary_sensor."""
    async_add_entities([EstFerieBinarySensor(), DemainFerieBinarySensor()])


class EstFerieBinarySensor(BinarySensorEntity):
    """Binary sensor : True si aujourd'hui est férié."""

    def __init__(self):
        self._attr_name = "Est Férié"
        self._attr_unique_id = f"{DOMAIN}_est_ferie"
        self._attr_icon = "mdi:calendar-star"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, "jourferier")},
            "name": "Jour Férié",
            "manufacturer": "xav59213",
            "model": "Capteur jours fériés dynamique",
            "sw_version": "1.0.6",
        }
        self._attr_is_on = False

    def update(self):
        """Mise à jour du statut."""
        today = date.today()
        holidays = get_holidays(today.year)
        self._attr_is_on = today in holidays

        self._attr_extra_state_attributes = {
            ATTR_HOLIDAY_NAME: holidays.get(today) if self._attr_is_on else "Aucun",
            ATTR_DATE: today.strftime("%d:%m"),
        }

    @property
    def is_on(self):
        """Retourne True si c'est un jour férié."""
        return self._attr_is_on


class DemainFerieBinarySensor(BinarySensorEntity):
    """Binary sensor : True si demain est férié."""

    def __init__(self):
        self._attr_name = "Demain est Férié"
        self._attr_unique_id = f"{DOMAIN}_demain_ferie"
        self._attr_icon = "mdi:calendar-arrow-right"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, "jourferier")},
            "name": "Jour Férié",
            "manufacturer": "xav59213",
            "model": "Capteur jours fériés dynamique",
            "sw_version": "1.0.6",
        }
        self._attr_is_on = False

    def update(self):
        """Mise à jour du statut."""
        tomorrow = date.today() + timedelta(days=1)
        holidays = get_holidays(tomorrow.year)
        self._attr_is_on = tomorrow in holidays

        self._attr_extra_state_attributes = {
            ATTR_HOLIDAY_NAME: holidays.get(tomorrow) if self._attr_is_on else "Aucun",
            ATTR_DATE: tomorrow.strftime("%d:%m"),
        }

    @property
    def is_on(self):
        """Retourne True si demain est un jour férié."""
        return self._attr_is_on
