# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os

import octoprint.plugin
import flask


class OctoLightShellPlugin(
        octoprint.plugin.StartupPlugin,
        octoprint.plugin.TemplatePlugin,
        octoprint.plugin.SimpleApiPlugin,
        octoprint.plugin.SettingsPlugin,
        octoprint.plugin.RestartNeedingPlugin
):

    light_state = False

    def get_settings_defaults(self):
        return dict(
            on_command = '',
            off_command = '',
        )

    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False)
        ]

    def on_after_startup(self):
        self.light_state = False
        os.system(self._settings.get(['off_command']))
        self._logger.info("OctoLightShell started")

    def on_api_get(self, request):
        self.light_state = not self.light_state
        if self.light_state:
            os.system(self._settings.get(['on_command']))
        else:
            os.system(self._settings.get(['off_command']))

        self._logger.info("Light state: {}".format(self.light_state))

        return flask.jsonify(status="ok")

    def get_update_information(self):
        return dict(
            octolight=dict(
                displayName="OctoLightShell",
                displayVersion=self._plugin_version,

                type="github_release",
                current=self._plugin_version,

                user="eternalgadgetry",
                repo="OctoLightShell",
                pip="https://github.com/eternalgadgetry/OctoLightShell/archive/{target}.zip"
            )
        )


__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = OctoLightShellPlugin()

__plugin_hooks__ = {
    "octoprint.plugin.softwareupdate.check_config":
    __plugin_implementation__.get_update_information
}
