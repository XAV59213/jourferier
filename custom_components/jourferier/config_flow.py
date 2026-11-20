"""Flux de configuration pour Jour Férié."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    CountrySelector,
    CountrySelectorConfig,
    LanguageSelector,
    LanguageSelectorConfig,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CONF_ALSACE_MOSELLE,
    CONF_COUNTRY,
    CONF_LANGUAGE,
    CONF_SUBDIVISION,
    DEFAULT_COUNTRY,
    DOMAIN,
    get_default_language,
    get_subdivision_options,
    get_supported_languages,
    holiday_settings_from_entry,
    list_holiday_countries,
    resolve_holiday_language,
)

_LOGGER = logging.getLogger(__name__)


def _supported_country_codes() -> list[str]:
    """Liste des codes pays proposés par holidays."""
    return sorted(list_holiday_countries().keys())


def _country_schema(default: str) -> vol.Schema:
    countries = _supported_country_codes()
    if default not in countries:
        default = DEFAULT_COUNTRY if DEFAULT_COUNTRY in countries else countries[0]
    return vol.Schema(
        {
            vol.Required(CONF_COUNTRY, default=default): CountrySelector(
                CountrySelectorConfig(countries=countries)
            )
        }
    )


def _details_schema(
    country: str,
    *,
    subdiv: str | None = None,
    language: str | None = None,
    alsace_moselle: bool = False,
) -> vol.Schema:
    """Schéma de la 2e étape (subdivision, langue, Alsace-Moselle si FR)."""
    schema: dict[Any, Any] = {}
    if options := get_subdivision_options(country):
        selector_options = [{"value": "", "label": "—"}] + options
        default_subdiv = subdiv if subdiv in {item["value"] for item in options} else ""
        schema[
            vol.Optional(CONF_SUBDIVISION, default=default_subdiv)
        ] = SelectSelector(
            SelectSelectorConfig(
                options=selector_options,
                mode=SelectSelectorMode.DROPDOWN,
            )
        )

    languages = get_supported_languages(country)
    if languages:
        default_lang = resolve_holiday_language(country, language) or get_default_language(
            country
        )
        if default_lang not in languages:
            default_lang = languages[0]
        schema[vol.Optional(CONF_LANGUAGE, default=default_lang)] = LanguageSelector(
            LanguageSelectorConfig(languages=languages)
        )

    if country == DEFAULT_COUNTRY:
        schema[vol.Optional(CONF_ALSACE_MOSELLE, default=alsace_moselle)] = bool

    return vol.Schema(schema)


def _options_from_input(country: str, user_input: dict[str, Any]) -> dict[str, Any]:
    """Construire les options à enregistrer."""
    subdiv = user_input.get(CONF_SUBDIVISION) or None
    language = user_input.get(CONF_LANGUAGE) or None
    alsace = bool(user_input.get(CONF_ALSACE_MOSELLE, False)) if country == DEFAULT_COUNTRY else False
    options: dict[str, Any] = {
        CONF_COUNTRY: country,
        CONF_ALSACE_MOSELLE: alsace,
    }
    if subdiv:
        options[CONF_SUBDIVISION] = subdiv
    if language:
        options[CONF_LANGUAGE] = language
    return options


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Gérer le flux de configuration."""

    VERSION = 2

    def __init__(self) -> None:
        self._country: str = DEFAULT_COUNTRY

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Étape 1 : choix du pays (France par défaut)."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_only")

        if user_input is not None:
            self._country = user_input[CONF_COUNTRY]
            details = await self.hass.async_add_executor_job(
                _details_schema, self._country
            )
            if details.schema:
                return await self.async_step_details()
            return self.async_create_entry(
                title="Jour Férié",
                data={},
                options=_options_from_input(self._country, {}),
            )

        schema = await self.hass.async_add_executor_job(
            _country_schema, DEFAULT_COUNTRY
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors={})

    async def async_step_details(self, user_input: dict[str, Any] | None = None):
        """Étape 2 : subdivision, langue et Alsace-Moselle (si France)."""
        if user_input is not None:
            return self.async_create_entry(
                title="Jour Férié",
                data={},
                options=_options_from_input(self._country, user_input),
            )

        default_language = None
        hass_language = getattr(self.hass.config, "language", None)
        if self._country == DEFAULT_COUNTRY:
            default_language = "fr"
        elif hass_language:
            default_language = hass_language

        def _schema():
            return _details_schema(
                self._country,
                language=default_language,
                alsace_moselle=False,
            )

        schema = await self.hass.async_add_executor_job(_schema)
        return self.async_show_form(step_id="details", data_schema=schema, errors={})

    @staticmethod
    @callback
    def async_get_options_flow(_config_entry: config_entries.ConfigEntry):
        """Retourner le flux d'options."""
        return OptionsFlowHandler()


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Flux d'options pour modifier le pays et les réglages après installation."""

    def __init__(self) -> None:
        self._country: str | None = None

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        """Étape 1 des options : pays."""
        if user_input is not None:
            self._country = user_input[CONF_COUNTRY]
            return await self.async_step_details()

        current = holiday_settings_from_entry(self.config_entry)
        schema = await self.hass.async_add_executor_job(
            _country_schema, current["country"]
        )
        return self.async_show_form(step_id="init", data_schema=schema)

    async def async_step_details(self, user_input: dict[str, Any] | None = None):
        """Étape 2 des options : subdivision, langue, Alsace-Moselle."""
        country = self._country or holiday_settings_from_entry(self.config_entry)["country"]
        current = holiday_settings_from_entry(self.config_entry)

        if user_input is not None:
            return self.async_create_entry(
                data=_options_from_input(country, user_input),
            )

        # Si le pays change, on ne reprend pas une subdivision devenue invalide.
        subdiv = current["subdiv"] if current["country"] == country else None
        language = current["language"] if current["country"] == country else None
        if country == DEFAULT_COUNTRY and language is None:
            language = "fr"
        alsace = current["alsace_moselle"] if country == DEFAULT_COUNTRY else False

        def _schema():
            return _details_schema(
                country,
                subdiv=subdiv,
                language=language,
                alsace_moselle=alsace,
            )

        schema = await self.hass.async_add_executor_job(_schema)
        return self.async_show_form(step_id="details", data_schema=schema)
