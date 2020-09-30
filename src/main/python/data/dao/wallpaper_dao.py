import sqlite3
import string
from os import path

import utils.utils as utils
from data.model.wallpaper_source_model import WallpaperSourceModel
from PyQt5 import QtCore

_mutex = QtCore.QMutex()


class WallpaperDAO:
    """
    Class used for persisting wallpaper relevant data like the history and sources.
    """

    def __init__(self):
        """
        Initializes the WPStore. Creates the database tables if they do not already exist.
        """
        self._database_url = path.join(utils.get_app_dir(), "wpstore.db")
        with QtCore.QMutexLocker(_mutex):
            conn = self.__connect()
            # create history table if it does not exist already
            c = conn.cursor()
            # c.execute("DROP TABLE IF EXISTS history")

            c.execute("CREATE TABLE IF NOT EXISTS history ("
                      "pk     INTEGER PRIMARY KEY,"
                      "uri    TEXT,"
                      "sourceid INTEGER,"
                      "ignored BOOLEAN);")

            c.execute("CREATE TABLE IF NOT EXISTS wpsources ("
                      "id    INTEGER PRIMARY KEY,"
                      "url  TEXT,"
                      "enabled BOOLEAN);")

            conn.commit()
            conn.close()

    def __connect(self):
        connection = sqlite3.connect(self._database_url)
        return connection

    def add_history_entry(self, entry: string, source_id: int):
        """
        Adds an entry to the history. Use the full path for the history to be able to compare it.

        :param entry: the full path to the wallpaper.
        """
        with QtCore.QMutexLocker(_mutex):
            conn = self.__connect()
            c = conn.cursor()
            c.execute("INSERT INTO history (uri, sourceid, ignored) VALUES (?,?, 'FALSE')", [entry, source_id])
            conn.commit()
            conn.close()

    def get_all(self, ignored: bool = False):
        """
        Returns all the history entries.

        :param ignored: if you want all ignored history entries of not ignored entries
        :return: a list of strings containing the full paths of the wallpapers
        """
        with QtCore.QMutexLocker(_mutex):
            ret = []
            conn = self.__connect()
            c = conn.cursor()
            for row in c.execute("SELECT uri FROM history WHERE ignored = ?", ['TRUE' if ignored else 'FALSE']):
                ret.append(row[0])
            conn.close()
            return ret

    def get_previous(self, index: int) -> string:
        """
        Returns the last added wallpaper of the history.

        :param index: the index counting back from the last added history entry (0: last, 1: second last, 2: third
        last, ...)
        :return: the path to the last wallpaper depending on the index or None if none was found.
        """
        with QtCore.QMutexLocker(_mutex):
            conn = self.__connect()
            c = conn.cursor()
            ret = c.execute("Select uri from history where pk = (select max(pk) from history) - ?", [index])
            entry = ret.fetchone()
            conn.close()
            if entry is None:
                return None
            else:
                return entry[0]

    def is_in_history(self, uri: string, ignored: bool = False):
        """
        Checks if uri is in history.

        :param uri: uri to check
        :param ignored: If true checks with all the ignored entries, else with all not ignored entries
        :return: true if it is in the ignored or not ignored history
        """
        with QtCore.QMutexLocker(_mutex):
            conn = self.__connect()
            ret = conn.execute("SELECT uri FROM history WHERE uri LIKE ? and ignored = ?", [uri, ignored])
            contains = ret.fetchone is not None
            conn.close()
            return contains

    def ignore_all(self):
        """
        Sets all not already ignored history entries to ignored.
        """
        with QtCore.QMutexLocker(_mutex):
            conn = self.__connect()
            c = conn.cursor()
            c.execute("UPDATE history SET ignored = 'TRUE' WHERE ignored = 'FALSE'")
            conn.commit()
            conn.close()

    def ignore_all_by_sourceid(self, source_id: int):
        with QtCore.QMutexLocker(_mutex):
            conn = self.__connect()
            c = conn.cursor()
            c.execute("UPDATE history SET ignored = 'TRUE' WHERE ignored = 'FALSE' and sourceid = ?", [source_id])
            conn.commit()
            conn.close()

    def get_sources(self, only_enabled=False):
        """
        Return a list of all the wallpaper sources.

        :param only_enabled: set to True if you only want the enabled sources.
        :return: a list of type WPSource of all the wallpaper sources.
        """
        with QtCore.QMutexLocker(_mutex):
            conn = self.__connect()
            c = conn.cursor()
            ret = []
            if only_enabled:
                # somehow TRUE does not work on windows using 1 instead
                for row in c.execute("SELECT * FROM wpsources WHERE enabled = 1;"):
                    ret.append(WallpaperSourceModel(row[0], row[1], row[2]))
            else:
                for row in c.execute("SELECT * FROM wpsources;"):
                    ret.append(WallpaperSourceModel(row[0], row[1], row[2]))
            conn.close()
            return ret

    def add_source(self, source: WallpaperSourceModel):
        """
        Adds the given source to the database.

        :param source: the source to add.
        """
        with QtCore.QMutexLocker(_mutex):
            conn = self.__connect()
            c = conn.cursor()
            c.execute("INSERT INTO wpsources (url, enabled) VALUES(?, ?);", [source.url, source.enabled])
            source.sid = c.lastrowid
            conn.commit()
            conn.close()

    def delete_source(self, source: WallpaperSourceModel):
        """
        Deletes the given source from the database.

        :param source: the source to delete
        """
        with QtCore.QMutexLocker(_mutex):
            conn = self.__connect()
            c = conn.cursor()
            c.execute("DELETE FROM wpsources WHERE id = ?;", [source.sid])
            conn.commit()
            conn.close()

    def update_source(self, source: WallpaperSourceModel):
        """
        Updates the given source in the database.

        :param source: the source to update
        """
        with QtCore.QMutexLocker(_mutex):
            conn = self.__connect()
            c = conn.cursor()
            c.execute("UPDATE wpsources SET url = ?, enabled = ? WHERE id = ?;",
                      [source.url, source.enabled, source.sid])
            conn.commit()
            conn.close()
