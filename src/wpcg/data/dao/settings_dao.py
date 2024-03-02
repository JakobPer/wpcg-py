# wpcg-py, a simple wallpaper changer
# Copyright (C) 2023  JakobPer
# 
# Full notice in Readme.md

import os
import json

from PySide6.QtCore import QMutex, QMutexLocker

from wpcg.data.model.settings_model import SettingsModel
import wpcg.utils.utils as utils


_mutex = QMutex()

class SettingsDAO:
    """
    Used to store and retrieve config parameters.
    """

    def __init__(self):
        """
        Creates the necessary tables in the database.
        """
        self._database_url = os.path.join(utils.get_app_dir(), "settings.json")

    def load(self) -> SettingsModel:
        if not os.path.exists(self._database_url):
            settings = SettingsModel()
            self.save(settings)
            return settings
        else:
            with QMutexLocker(_mutex):
                with  open(self._database_url, "r") as file:
                    content = json.load(file)
                    return SettingsModel(**content)


    def save(self, settings: SettingsModel) -> None:
        with QMutexLocker(_mutex):
            with open(self._database_url, "w") as file:
                json.dump(settings.__dict__, file, indent=4)

