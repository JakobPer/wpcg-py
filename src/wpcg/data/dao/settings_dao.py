# wpcg-py, a simple wallpaper changer
# Copyright (C) 2023  JakobPer
# 
# Full notice in Readme.md

import os
import json

from PySide6.QtCore import QMutex, QMutexLocker

from wpcg.data.model.settings_model import *
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
        self._app_settings_path = os.path.join(utils.get_app_dir(), "appsettings.json")

    def load_app_settings(self) -> AppSettingsModel:
        if not os.path.exists(self._app_settings_path):
            appsettings = AppSettingsModel()
            self.save_app_settings(appsettings)
            return appsettings
        else:
            with QMutexLocker(_mutex):
                with open(self._app_settings_path, "r") as file:
                    content = json.load(file)
                    return AppSettingsModel(**content)

    def save_app_settings(self, appsettings: AppSettingsModel) -> None:
        with QMutexLocker(_mutex):
            with open(self._app_settings_path, "w") as file:
                json.dump(appsettings.__dict__, file, indent=4)

    def load_shared(self, appsettings: AppSettingsModel) -> SharedSettingsModel:
        settings_file = os.path.join(appsettings.base_dir, "settings.json")
        if not os.path.exists(settings_file):
            settings = SharedSettingsModel()
            self.save_shared(settings)
            return settings
        else:
            with QMutexLocker(_mutex):
                with  open(settings_file, "r") as file:
                    content = json.load(file)
                    return SharedSettingsModel(**content)


    def save_shared(self, settings: SharedSettingsModel, appsettings: AppSettingsModel) -> None:
        settings_file = os.path.join(appsettings.base_dir, "settings.json")
        with QMutexLocker(_mutex):
            with open(settings_file, "w") as file:
                json.dump(settings.__dict__, file, indent=4)

