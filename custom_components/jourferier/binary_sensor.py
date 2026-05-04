"""Binary sensor pour indiquer si aujourd'hui est un jour férié."""
import logging
from datetime import date
from homeassistant.components.binary_sensor import BinarySensorEntity
from .const import DOMAIN, get_holidays

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Configurer la plateforme binary_sensor."""
    async_add_entities([EstFerieBinarySensor()])


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

        # Optionnel : tu peux ajouter l'attribut avec le nom du jour férié
        if self._attr_is_on:
            self._attr_extra_state_attributes = {
                "holiday_name": holidays[today]
            }
        else:
            self._attr_extra_state_attributes = {}

    @property
    def is_on(self):
        """Retourne True si c'est un jour férié."""
        return self._attr_is_on
