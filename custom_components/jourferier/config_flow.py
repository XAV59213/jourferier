"""Flux de configuration pour Jour Férié."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from .const import CONF_ALSACE_MOSELLE, DOMAIN

_LOGGER = logging.getLogger(__name__)

ALSACE_MOSELLE_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_ALSACE_MOSELLE, default=False): bool,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Gérer le flux de configuration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Gérer l'étape utilisateur."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_only")

        if user_input is not None:
            return self.async_create_entry(
                title="Jour Férié",
                data={},
                options={
                    CONF_ALSACE_MOSELLE: user_input.get(CONF_ALSACE_MOSELLE, False),
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=ALSACE_MOSELLE_SCHEMA,
            description_placeholders={"description": "Souhaitez-vous activer le capteur de jour férié ?"},
            errors={},
        )

    @staticmethod
    def async_get_options_flow(_config_entry: config_entries.ConfigEntry):
        """Retourner le flux d'options."""
        return OptionsFlowHandler()


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Flux d'options pour modifier l'intégration après installation."""

    async def async_step_init(self, user_input=None):
        """Gérer les options."""
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_ALSACE_MOSELLE,
                        default=self.config_entry.options.get(CONF_ALSACE_MOSELLE, False),
                    ): bool,
                }
            ),
        )
