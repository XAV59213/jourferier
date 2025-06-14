"""Capteur de calendrier pour les jours fériés."""
import logging
from datetime import datetime
from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util
from .const import DOMAIN, PUBLIC_HOLIDAYS_2025, HOLIDAY_DESCRIPTIONS

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configurer l'entité calendrier à partir d'une entrée de configuration."""
    _LOGGER.info("Configuration de la plateforme calendrier pour %s", config_entry.entry_id)
    try:
        async_add_entities([JourFerieCalendar(config_entry)], update_before_add=False)
        _LOGGER.info("Entité calendrier ajoutée avec succès")
    except Exception as e:
        _LOGGER.exception("Erreur lors de la configuration de la plateforme calendrier : %s", e)
        raise

class JourFerieCalendar(CalendarEntity):
    """Entité calendrier pour les jours fériés."""

    def __init__(self, config_entry: ConfigEntry):
        """Initialiser le calendrier des jours fériés."""
        _LOGGER.debug("Initialisation de JourFerieCalendar")
        self._config_entry = config_entry
        self._attr_name = "Calendrier des Jours Fériés"
        self._attr_unique_id = "calendrier_des_jours_feries"  # Identifiant fixe
        self._events = self._generate_events()

    def _generate_events(self) -> list[CalendarEvent]:
        """Générer les événements de calendrier pour les jours fériés de 2025."""
        _LOGGER.debug("Génération des événements pour les jours fériés")
        events = []
        current_year = 2025

        for date_str, holiday_name in PUBLIC_HOLIDAYS_2025.items():
            try:
                day, month = map(int, date_str.split(":"))
                event_date = datetime(current_year, month, day, tzinfo=dt_util.DEFAULT_TIME_ZONE)
                description = HOLIDAY_DESCRIPTIONS.get(holiday_name, "")
                
                events.append(
                    CalendarEvent(
                        summary=holiday_name,
                        description=description,
                        start=event_date.replace(hour=0, minute=0, second=0),
                        end=event_date.replace(hour=23, minute=59, second=59),
                    )
                )
                _LOGGER.debug("Événement ajouté : %s (%s)", holiday_name, event_date)
            except ValueError as e:
                _LOGGER.error("Erreur lors de la création de l'événement pour %s : %s", date_str, e)

        _LOGGER.debug("Événements générés : %s", len(events))
        return sorted(events, key=lambda x: x.start)

    @property
    def event(self) -> CalendarEvent | None:
        """Retourner l'événement en cours ou le prochain événement."""
        now = dt_util.now()
        for event in self._events:
            if event.start <= now < event.end:
                _LOGGER.debug("Événement en cours trouvé : %s", event.summary)
                return event
            if event.start > now:
                _LOGGER.debug("Prochain événement trouvé : %s", event.summary)
                return event
        _LOGGER.debug("Aucun événement trouvé")
        return None

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        """Retourner les événements dans une plage de dates donnée."""
        events = [
            event for event in self._events
            if event.start >= start_date and event.end <= end_date
        ]
        _LOGGER.debug("Événements récupérés pour %s à %s : %s", start_date, end_date, len(events))
        return events
