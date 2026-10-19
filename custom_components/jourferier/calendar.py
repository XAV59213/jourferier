"""Capteur de calendrier pour les jours fériés."""
import logging
from datetime import datetime, date
from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util
from .const import DOMAIN, get_holidays, HOLIDAY_DESCRIPTIONS

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
        self._attr_unique_id = "calendrier_des_jours_feries"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, "jourferier")},
            "name": "Jour Férié",
            "manufacturer": "xav59213",
        }

    def _generate_events_for_years(self, start_year: int, end_year: int) -> list[CalendarEvent]:
        """Générer les événements pour une plage d'années."""
        events = []
        for year in range(start_year, end_year + 1):
            holidays = get_holidays(year)
            for holiday_date, name in holidays.items():
                try:
                    event_date = datetime.combine(
                        holiday_date, datetime.min.time(), tzinfo=dt_util.DEFAULT_TIME_ZONE
                    )
                    description = HOLIDAY_DESCRIPTIONS.get(name, "")
                    events.append(
                        CalendarEvent(
                            summary=name,
                            description=description,
                            start=event_date.replace(hour=0, minute=0),
                            end=event_date.replace(hour=23, minute=59),
                        )
                    )
                except Exception as e:
                    _LOGGER.error("Erreur lors de la création de l'événement %s : %s", name, e)
        return sorted(events, key=lambda x: x.start)

    @property
    def event(self) -> CalendarEvent | None:
        """Retourner l'événement en cours ou le prochain événement."""
        now = dt_util.now()
        current_year = now.year
        # Génère pour l'année courante et la suivante pour avoir le prochain
        events = self._generate_events_for_years(current_year, current_year + 1)
        for ev in events:
            if ev.start <= now < ev.end:
                return ev
            if ev.start > now:
                return ev
        return None

    async def async_get_events(self, hass, start_date, end_date) -> list[CalendarEvent]:
        """Retourner les événements entre deux dates."""
        # Convertir en date si nécessaire
        if isinstance(start_date, datetime):
            start_date = start_date.date()
        if isinstance(end_date, datetime):
            end_date = end_date.date()

        start_year = start_date.year
        end_year = end_date.year
        events = self._generate_events_for_years(start_year, end_year)
        return [e for e in events if start_date <= e.start.date() <= end_date]
