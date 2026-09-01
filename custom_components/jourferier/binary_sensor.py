"""Binary sensors pour indiquer si aujourd'hui ou demain est un jour férié."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.util import dt as dt_util

from .const import ATTR_DATE, ATTR_HOLIDAY_NAME, DOMAIN, get_device_info, get_holidays


async def async_setup_entry(hass, entry, async_add_entities):
    """Configurer la plateforme binary_sensor."""
    async_add_entities([EstFerieBinarySensor(), DemainFerieBinarySensor()])


class _HolidayBinarySensor(BinarySensorEntity):
    """Base commune pour les binary sensors jours fériés."""

    _attr_has_entity_name = True
    _offset_days = 0

    def __init__(self) -> None:
        self._attr_device_info = get_device_info()
        self._attr_is_on = False
        self._attr_extra_state_attributes = {}

    def update(self) -> None:
        target = dt_util.now().date() + timedelta(days=self._offset_days)
        holidays = get_holidays(target.year)
        self._attr_is_on = target in holidays
        self._attr_extra_state_attributes = {
            ATTR_HOLIDAY_NAME: holidays.get(target, "Aucun"),
            ATTR_DATE: target.strftime("%d:%m"),
        }


class EstFerieBinarySensor(_HolidayBinarySensor):
    """True si aujourd'hui est férié."""

    _attr_name = "Est Férié"
    _attr_translation_key = "est_ferie"
    _attr_unique_id = f"{DOMAIN}_est_ferie"
    _attr_icon = "mdi:calendar-star"
    _offset_days = 0


class DemainFerieBinarySensor(_HolidayBinarySensor):
    """True si demain est férié."""

    _attr_name = "Demain est Férié"
    _attr_translation_key = "demain_est_ferie"
    _attr_unique_id = f"{DOMAIN}_demain_ferie"
    _attr_icon = "mdi:calendar-arrow-right"
    _offset_days = 1
