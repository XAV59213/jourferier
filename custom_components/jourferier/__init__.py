"""Composant Jour Férié pour Home Assistant."""
import logging
import json
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.const import CONF_NAME
from homeassistant.helpers import config_validation as cv
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Définir un schéma vide pour indiquer que l'intégration est gérée via config_flow
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Configurer le composant."""
    _LOGGER.info("Initialisation de %s", DOMAIN)
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configurer une entrée de configuration."""
    _LOGGER.info("Configuration de l'entrée pour %s", DOMAIN)
    try:
        # Configurer les plateformes sensor et calendar
        _LOGGER.debug("Chargement des plateformes : sensor, calendar")
        await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "calendar"])
        _LOGGER.info("Plateformes sensor et calendar configurées avec succès")
    except Exception as e:
        _LOGGER.error("Erreur lors de la configuration des plateformes : %s", e)
        raise ConfigEntryNotReady from e

    async def handle_create_card_service(call):
        """Service pour ajouter une carte Lovelace."""
        lovelace_path = hass.config.path(".storage/lovelace")
        try:
            with open(lovelace_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            new_card = {
                "type": "entity",
                "entity": "sensor.jour_ferie",
                "name": "Jour Férié",
                "icon": "mdi:calendar-star"
            }
            data["data"]["config"]["views"][0]["cards"].append(new_card)
            with open(lovelace_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            _LOGGER.info("Carte Lovelace 'Jour Férié' ajoutée avec succès.")
        except Exception as e:
            _LOGGER.error("Erreur lors de l’ajout de la carte Lovelace : %s", e)

    hass.services.async_register(DOMAIN, "create_card", handle_create_card_service)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Décharger une entrée de configuration."""
    _LOGGER.info("Déchargement des plateformes pour %s", DOMAIN)
    return await hass.config_entries.async_unload_platforms(entry, ["sensor", "calendar"])
