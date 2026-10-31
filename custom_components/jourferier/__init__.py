"""Composant Jour Férié pour Home Assistant."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import config_validation as cv
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor", "calendar", "binary_sensor"]

# Définir un schéma vide pour indiquer que l'intégration est gérée via config_flow
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Configurer le composant."""
    _LOGGER.info("Initialisation de %s", DOMAIN)
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configurer une entrée de configuration."""
    _LOGGER.info("Configuration de l'entrée pour %s", DOMAIN)
    domain_data = hass.data.setdefault(DOMAIN, {})
    if not domain_data.get("frontend_registered"):
        from .frontend import JSModuleRegistration

        try:
            await JSModuleRegistration(hass).async_register()
            domain_data["frontend_registered"] = True
        except Exception:  # noqa: BLE001
            _LOGGER.exception("Échec d'enregistrement de la carte Lovelace")
    try:
        _LOGGER.debug("Chargement des plateformes : %s", ", ".join(PLATFORMS))
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
        _LOGGER.info("Plateformes %s configurées avec succès", ", ".join(PLATFORMS))
    except Exception as e:
        _LOGGER.error("Erreur lors de la configuration des plateformes : %s", e)
        raise ConfigEntryNotReady from e

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Décharger une entrée de configuration."""
    _LOGGER.info("Déchargement des plateformes pour %s", DOMAIN)
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
