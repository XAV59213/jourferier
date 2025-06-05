"""Composant Jour Férié pour Home Assistant."""
import logging
import json
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    _LOGGER.info("Initialisation de %s", DOMAIN)
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    try:
        await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    except Exception as e:
        _LOGGER.error("Erreur lors de la configuration du sensor : %s", e)
        raise ConfigEntryNotReady from e

    async def handle_create_card_service(call):
        lovelace_path = hass.config.path(".storage/lovelace")
        try:
            with open(lovelace_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            new_card = {"type": "entity", "entity": "sensor.jour_ferie", "name": "Jour Férié", "icon": "mdi:calendar-star"}
            data["data"]["config"]["views"][0]["cards"].append(new_card)
            with open(lovelace_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            _LOGGER.info("Carte Lovelace 'Jour Férié' ajoutée avec succès.")
        except Exception as e:
            _LOGGER.error("Erreur lors de l’ajout de la carte Lovelace : %s", e)

    hass.services.async_register(DOMAIN, "create_card", handle_create_card_service)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, ["sensor"])