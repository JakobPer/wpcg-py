import os
import sqlite3
import string

import utils.utils as utils

from PyQt5 import QtCore

_mutex = QtCore.QMutex()


class ConfigDAO:
    """
    Used to store and retrieve config parameters.
    """

    KEY_INTERVAL = "INTERVAL"
    KEY_NSFW = "NSFW"
    KEY_PRETTIFICATION_THRESHOLD = "PRETTIFICATION_THRESHOLD"
    KEY_PRETTIFICATION_ENABLED = "PRETTIFICATION_ENABLED"
    KEY_REPEAT_BACKGROUND_ENABLED = "REPEAT_BACKGROUND_ENABLED"
    KEY_BLUR_BACKGROUND_ENABLED = "BLUR_BACKGROUND_ENABLED"
    KEY_BLEND_EDGES_ENABLED = "BLEND_EDGES_ENABLED"
    KEY_WALLPAPER_WIDTH = "WALLPAPER_WIDTH"
    KEY_WALLPAPER_HEIGHT = "WALLPAPER_HEIGHT"
    KEY_BLUR_AMOUNT = "BLUR_AMOUNT"
    KEY_BLEND_RATIO = "BLEND_RATIO"

    def __init__(self):
        """
        Creates the necessary tables in the database.
        """
        self._database_url = os.path.join(utils.get_app_dir(), "wpconfig.db")
        with QtCore.QMutexLocker(_mutex):
            conn = self.__connect()
            # create history table
            c = conn.cursor()
            # c.execute("DROP TABLE IF EXISTS config")
            c.execute("CREATE TABLE IF NOT EXISTS config ("
                      "key    TEXT PRIMARY KEY,"
                      "value  TEXT);")
            conn.commit()
            conn.close()

    def __connect(self):
        connection = sqlite3.connect(self._database_url)
        return connection

    def get(self, key: string, default=None) -> string:
        """
        Retrieves the setting from the database but returns the default if the key could not be found.

        :param key: the key of the setting
        :param default: the default value returned when the key could not be found
        :return: the setting or default if key could not be found
        """
        with QtCore.QMutexLocker(_mutex):
            conn = self.__connect()
            ret = conn.execute("SELECT value FROM config WHERE key LIKE ?", [key])
            entry = ret.fetchone()
            conn.close()

            if entry is None:
                return default
            else:
                return entry[0]

    def set(self, key: string, value: string):
        """
        Sets or updates the setting of the key.

        :param key: the key of the setting
        :param value: the value of the setting
        """
        with QtCore.QMutexLocker(_mutex):
            conn = self.__connect()
            c = conn.cursor()
            c.execute("REPLACE INTO config VALUES (?, ?)", [key, value])
            conn.commit()
            conn.close()

    def contains_key(self, key: string) -> bool:
        """
        Checks if the database contains the key.

        :param key: the key to check
        :return: True if the key is in the database else False
        """
        with QtCore.QMutexLocker(_mutex):
            conn = self.__connect()
            ret = conn.execute("SELECT * FROM config WHERE key LIKE ?", [key])
            contains = ret.fetchone() is not None
            conn.close()

            return contains
