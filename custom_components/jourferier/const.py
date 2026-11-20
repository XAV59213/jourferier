"""Constantes pour le composant Jour Férié."""
from __future__ import annotations

from datetime import date, timedelta
from functools import lru_cache
from typing import Any

DOMAIN = "jourferier"
CONF_ALSACE_MOSELLE = "alsace_moselle"
CONF_COUNTRY = "country"
CONF_SUBDIVISION = "subdivision"
CONF_LANGUAGE = "language"
DEFAULT_COUNTRY = "FR"
SENSOR_NAME = "Jour Férié"
SENSOR_UNIQUE_ID = f"{DOMAIN}_sensor"
ATTR_HOLIDAY_NAME = "holiday_name"
ATTR_DATE = "date"
ATTR_NEXT_HOLIDAY = "next_holiday"
ATTR_DAYS_UNTIL = "days_until"
ATTR_PROCHAIN_PONT_POTENTIEL = "prochain_pont_potentiel"
VERSION = "1.3.1"
MANUFACTURER = "xav59213"
DEVICE_MODEL = "Capteur jours fériés dynamique"
DEVICE_URL = "https://github.com/XAV59213/jourferier"

# Libellés historiques conservés pour la France (indépendants des intitulés de la
# bibliothèque holidays, dont la typographie et certains noms diffèrent).
_FR_NAME_MAP = {
    "jour de l'an": "Jour de l’An",
    "lundi de paques": "Lundi de Pâques",
    "lundi de pâques": "Lundi de Pâques",
    "fete du travail": "Fête du Travail",
    "fête du travail": "Fête du Travail",
    "fete de la victoire": "Victoire 1945",
    "fête de la victoire": "Victoire 1945",
    "victoire 1945": "Victoire 1945",
    "ascension": "Ascension",
    "lundi de pentecote": "Lundi de Pentecôte",
    "lundi de pentecôte": "Lundi de Pentecôte",
    "fete nationale": "Fête Nationale",
    "fête nationale": "Fête Nationale",
    "assomption": "Assomption",
    "toussaint": "Toussaint",
    "armistice": "Armistice 1918",
    "armistice 1918": "Armistice 1918",
    "noel": "Noël",
    "noël": "Noël",
    "vendredi saint": "Vendredi Saint",
    "saint-etienne": "Saint Étienne",
    "saint-étienne": "Saint Étienne",
    "saint etienne": "Saint Étienne",
    "saint étienne": "Saint Étienne",
}

# Libellés de secours pour les subdivisions FR des anciennes versions de holidays.
FR_SUBDIV_LABELS = {
    "57": "Moselle",
    "6AE": "Alsace",
    "GES": "Grand Est / Alsace-Moselle",
    "971": "Guadeloupe",
    "GP": "Guadeloupe",
    "972": "Martinique",
    "MQ": "Martinique",
    "973": "Guyane",
    "GY": "Guyane",
    "974": "La Réunion",
    "RE": "La Réunion",
    "976": "Mayotte",
    "YT": "Mayotte",
    "BL": "Saint-Barthélemy",
    "MF": "Saint-Martin",
    "NC": "Nouvelle-Calédonie",
    "PF": "Polynésie Française",
    "PM": "Saint-Pierre-et-Miquelon",
    "TF": "Terres australes françaises",
    "WF": "Wallis-et-Futuna",
}


def get_device_info() -> dict:
    """Infos appareil partagées par toutes les entités."""
    return {
        "identifiers": {(DOMAIN, "jourferier")},
        "name": "Jour Férié",
        "manufacturer": MANUFACTURER,
        "model": DEVICE_MODEL,
        "sw_version": VERSION,
        "configuration_url": DEVICE_URL,
    }


def _import_holidays():
    """Importer holidays à la demande (absent au chargement / durant hassfest)."""
    import holidays

    return holidays


def list_holiday_countries() -> dict[str, list[str]]:
    """Pays et subdivisions supportés par la bibliothèque holidays."""
    return _import_holidays().list_supported_countries(include_aliases=False)


def holiday_settings_from_entry(entry: Any) -> dict[str, Any]:
    """Extraire les réglages de calcul depuis une config entry.

    Un pays absent vaut la France. L'option Alsace-Moselle déjà enregistrée
    est conservée telle quelle (False si la clé n'existe pas).
    """
    options = getattr(entry, "options", {}) or {}
    data = getattr(entry, "data", {}) or {}
    country = options.get(CONF_COUNTRY) or data.get(CONF_COUNTRY) or DEFAULT_COUNTRY
    subdiv = options.get(CONF_SUBDIVISION, data.get(CONF_SUBDIVISION))
    if subdiv == "":
        subdiv = None
    language = options.get(CONF_LANGUAGE, data.get(CONF_LANGUAGE))
    if language == "":
        language = None
    alsace = bool(options.get(CONF_ALSACE_MOSELLE, False))
    return {
        "country": country,
        "subdiv": subdiv,
        "language": language,
        "alsace_moselle": alsace,
    }


def is_alsace_moselle(entry: Any) -> bool:
    """Retourne True si l'option Alsace-Moselle est activée."""
    return bool(holiday_settings_from_entry(entry)["alsace_moselle"])


def _normalize_holiday_name(name: str) -> str:
    """Normaliser un nom pour le rapprocher des libellés historiques FR."""
    normalized = (
        name.replace("’", "'")
        .replace("‘", "'")
        .replace("`", "'")
        .strip()
        .casefold()
    )
    return (
        normalized.replace("é", "e")
        .replace("è", "e")
        .replace("ê", "e")
        .replace("ë", "e")
        .replace("à", "a")
        .replace("â", "a")
        .replace("î", "i")
        .replace("ï", "i")
        .replace("ô", "o")
        .replace("ù", "u")
        .replace("û", "u")
        .replace("ç", "c")
    )


def _display_name(country: str, name: str) -> str:
    """Conserver les libellés FR historiques lorsque le nom est reconnu."""
    if country != DEFAULT_COUNTRY:
        return name
    mapped = _FR_NAME_MAP.get(name.casefold()) or _FR_NAME_MAP.get(
        _normalize_holiday_name(name)
    )
    return mapped or name


def resolve_holiday_language(country: str, configured: str | None) -> str | None:
    """Choisir une langue supportée par holidays (ou la langue par défaut du pays)."""
    holidays = _import_holidays()
    obj = holidays.country_holidays(country)
    supported = tuple(getattr(obj, "supported_languages", ()) or ())
    if not supported:
        return None
    default = getattr(obj, "default_language", None)

    def _match(lang: str | None) -> str | None:
        if not lang:
            return None
        if lang in supported:
            return lang
        underscored = lang.replace("-", "_")
        if underscored in supported:
            return underscored
        primary = underscored.split("_", 1)[0]
        if primary in supported:
            return primary
        for item in supported:
            if item == primary or item.startswith(f"{primary}_"):
                return item
        return None

    return _match(configured) or default


@lru_cache(maxsize=1)
def alsace_moselle_subdiv() -> str:
    """Code de subdivision holidays pour l'Alsace-Moselle.

    Le code officiel a changé selon les versions de la bibliothèque :
    ``6AE`` / ``57`` (récentes, sans avertissement) ou ``GES`` (HA 2024.6,
    holidays 0.50). ``Alsace-Moselle`` fonctionne encore mais est déprécié
    et n'est utilisé qu'en dernier recours.
    """
    holidays = _import_holidays()
    supported = set(
        holidays.list_supported_countries(include_aliases=False).get("FR", []) or []
    )
    alias_names: set[str] = set()
    alias_targets: set[str] = set()
    try:
        raw = getattr(holidays.country_holidays("FR"), "subdivisions_aliases", None) or {}
        alias_names = set(raw.keys())
        alias_targets = {str(value) for value in raw.values()}
    except Exception:  # noqa: BLE001
        pass

    for candidate in ("6AE", "57"):
        if candidate in supported or candidate in alias_targets:
            return candidate if candidate in supported else candidate
    for candidate, target in (("Alsace", "6AE"), ("Moselle", "57")):
        if candidate in alias_names and target in supported:
            return target
        if candidate in supported:
            return candidate
    if "GES" in supported:
        return "GES"
    return "Alsace-Moselle"


def effective_subdivision(
    country: str,
    subdiv: str | None,
    alsace_moselle: bool = False,
) -> str | None:
    """Subdivision réellement transmise à holidays."""
    if subdiv:
        return subdiv
    if country == DEFAULT_COUNTRY and alsace_moselle:
        return alsace_moselle_subdiv()
    return None


def get_subdivision_options(country: str) -> list[dict[str, str]]:
    """Options de sélection des subdivisions, avec libellés si disponibles."""
    holidays = _import_holidays()
    provinces = list_holiday_countries().get(country) or []
    if not provinces:
        return []

    labels: dict[str, str] = {}
    if country == DEFAULT_COUNTRY:
        labels.update(FR_SUBDIV_LABELS)
    try:
        obj = holidays.country_holidays(country)
        get_aliases = getattr(obj, "get_subdivision_aliases", None)
        aliases = get_aliases() if get_aliases else None
        if aliases:
            for code, names in aliases.items():
                if isinstance(names, (list, tuple)):
                    label = ", ".join(str(item) for item in names if item)
                else:
                    label = str(names) if names else ""
                if label:
                    labels[str(code)] = label
    except Exception:  # noqa: BLE001
        pass

    options: list[dict[str, str]] = []
    seen: set[str] = set()
    for code in provinces:
        if code in seen:
            continue
        seen.add(code)
        options.append({"value": code, "label": labels.get(code, code)})
    return options


def get_supported_languages(country: str) -> list[str]:
    """Langues proposées par holidays pour un pays, éventuellement vide."""
    obj = _import_holidays().country_holidays(country)
    return list(getattr(obj, "supported_languages", ()) or ())


def get_default_language(country: str) -> str | None:
    """Langue par défaut de holidays pour un pays."""
    obj = _import_holidays().country_holidays(country)
    return getattr(obj, "default_language", None)


def get_holidays(
    year: int,
    alsace_moselle: bool = False,
    *,
    country: str = DEFAULT_COUNTRY,
    subdiv: str | None = None,
    language: str | None = None,
) -> dict[date, str]:
    """Retourne les jours fériés d'une année pour le pays (et la subdivision) choisis.

    Tous les capteurs, le calendrier et le calcul des ponts passent par cette
    fonction. Pour la France, les noms historiques de l'intégration sont
    conservés. L'option Alsace-Moselle (France uniquement, si aucune autre
    subdivision n'est choisie) s'appuie sur le code holidays le plus robuste
    disponible (``6AE`` / ``57`` ou ``GES``).
    """
    holidays = _import_holidays()
    country = country or DEFAULT_COUNTRY
    used_subdiv = effective_subdivision(country, subdiv, alsace_moselle)
    used_language = resolve_holiday_language(country, language)
    kwargs: dict[str, Any] = {"country": country, "years": year}
    if used_subdiv:
        kwargs["subdiv"] = used_subdiv
    if used_language:
        kwargs["language"] = used_language
    raw = holidays.country_holidays(**kwargs)
    return {
        holiday_date: _display_name(country, name)
        for holiday_date, name in raw.items()
        if holiday_date.year == year
    }


def is_day_off(
    target_date: date,
    alsace_moselle: bool = False,
    *,
    country: str = DEFAULT_COUNTRY,
    subdiv: str | None = None,
    language: str | None = None,
) -> bool:
    """Retourne True si la date est un week-end ou un jour férié."""
    return target_date.weekday() >= 5 or target_date in get_holidays(
        target_date.year,
        alsace_moselle,
        country=country,
        subdiv=subdiv,
        language=language,
    )


def get_next_potential_bridge(
    today: date,
    alsace_moselle: bool = False,
    *,
    country: str = DEFAULT_COUNTRY,
    subdiv: str | None = None,
    language: str | None = None,
) -> date | None:
    """Retourne la date du prochain jour ouvré entre deux jours de repos."""
    kwargs = {
        "alsace_moselle": alsace_moselle,
        "country": country,
        "subdiv": subdiv,
        "language": language,
    }
    for offset in range(1, 367):
        pont_potentiel = today + timedelta(days=offset)
        if (
            not is_day_off(pont_potentiel, **kwargs)
            and is_day_off(pont_potentiel - timedelta(days=1), **kwargs)
            and is_day_off(pont_potentiel + timedelta(days=1), **kwargs)
        ):
            return pont_potentiel

    return None


HOLIDAY_DESCRIPTIONS = {
    "Jour de l’An": "Bonne année ! Que cette nouvelle année soit pleine de joie et de réussite !",
    "Lundi de Pâques": "Joyeuses Pâques ! Profitez de cette journée festive en famille !",
    "Fête du Travail": "Bonne fête du travail ! Une journée pour célébrer les travailleurs !",
    "Victoire 1945": "Hommage à la victoire de 1945 ! Une journée de mémoire et de paix.",
    "Ascension": "Joyeuse Ascension ! Une journée spirituelle et de repos.",
    "Lundi de Pentecôte": "Bonne fête de Pentecôte ! Une journée pour célébrer l'Esprit Saint.",
    "Fête Nationale": "Vive la France ! Joyeux 14 juillet, fête nationale !",
    "Assomption": "Bonne fête de l’Assomption ! Une journée de célébration mariale.",
    "Toussaint": "Bonne Toussaint ! Un moment pour honorer les saints et les défunts.",
    "Armistice 1918": "Hommage aux héros de 1918 ! Une journée de recueillement.",
    "Noël": "Joyeux Noël ! Une fête chaleureuse pour partager amour et cadeaux !",
    "Vendredi Saint": "Vendredi Saint : une journée de recueillement, fériée en Alsace-Moselle.",
    "Saint Étienne": "Bonne fête de la Saint-Étienne ! Un jour férié observé en Alsace-Moselle.",
}

# Carte Lovelace native
URL_BASE = f"/{DOMAIN}"
CARD_FILENAME = "jour-ferie-card.js"
CARD_TAG = "jour-ferie-card"
STATIC_CARD_PATH = f"{URL_BASE}/{CARD_FILENAME}"
