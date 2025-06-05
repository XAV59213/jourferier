"""Flux de configuration pour Jour Férié."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_only")

        if user_input is not None:
            return self.async_create_entry(title="Jour Férié", data={})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
            description_placeholders={"description": "Souhaitez-vous activer le capteur de jour férié ?"},
            errors={}
        )