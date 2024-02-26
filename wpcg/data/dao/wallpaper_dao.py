# wpcg-py, a simple wallpaper changer
# Copyright (C) 2023  JakobPer
# 
# Full notice in Readme.md

import string
from typing import List
from os import path

import utils.utils as utils
from data.model.wallpaper_source_model import WallpaperSourceModel, HistoryModel, Base
from PySide6 import QtCore

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

_mutex = QtCore.QMutex()


class WallpaperDAO:
    """
    Class used for persisting wallpaper relevant data like the history and sources.
    """

    def __init__(self):
        """
        Initializes the WPStore. Creates the database tables if they do not already exist.
        """
        self._database_url = "sqlite:///" + path.join(utils.get_app_dir(), "database.db")
        with QtCore.QMutexLocker(_mutex):
            self._engine = self.__connect()
            self._session = Session(self._engine)
            Base.metadata.create_all(self._engine)

    def __connect(self):
        connection = create_engine(self._database_url, echo=True)
        return connection

    def close(self):
        self._session.flush()
        self._session.close()

    def add_history_entry(self, entry: string, wallpaper_source: WallpaperSourceModel):
        """
        Adds an entry to the history. Use the full path for the history to be able to compare it.

        :param entry: the full path to the wallpaper.
        """
        with QtCore.QMutexLocker(_mutex):
            entry = HistoryModel(entry, wallpaper_source)
            self._session.add(entry)
            self._session.commit()

    def get_all(self, ignored: bool = False) -> List[HistoryModel]:
        """
        Returns all the history entries.

        :param ignored: if you want all ignored history entries of not ignored entries
        :return: a list of strings containing the full paths of the wallpapers
        """
        with QtCore.QMutexLocker(_mutex):
            stmt = select(HistoryModel).where(HistoryModel.is_ignored == ignored)
            return [x for x in self._session.scalars(stmt)]


    def get_previous(self, index: int) -> HistoryModel:
        """
        Returns the last added wallpaper of the history.

        :param index: the index counting back from the last added history entry (0: last, 1: second last, 2: third
        last, ...)
        :return: the path to the last wallpaper depending on the index or None if none was found.
        """
        with QtCore.QMutexLocker(_mutex):
            stmt = select(HistoryModel).order_by(HistoryModel.id.desc())
            entries = self._session.scalars(stmt).all()
            if entries is None:
                return None
            else:
                return entries[index] if index >= 0 and index < len(entries) else None

    def is_in_history(self, uri: string, ignored: bool = False):
        """
        Checks if uri is in history.

        :param uri: uri to check
        :param ignored: If true checks with all the ignored entries, else with all not ignored entries
        :return: true if it is in the ignored or not ignored history
        """
        with QtCore.QMutexLocker(_mutex):
            stmt = select(HistoryModel).where(HistoryModel.entry == uri, HistoryModel.is_ignored == ignored )
            ret = self._session.scalars(stmt).first()
            return ret is not None

    def ignore_all(self):
        """
        Sets all not already ignored history entries to ignored.
        """
        with QtCore.QMutexLocker(_mutex):
            stmt = select(HistoryModel).where(HistoryModel.is_ignored == False)
            for entry in self._session.scalars(stmt):
                entry.is_ignored = True
            self._session.commit()

    def ignore_all_by_sourceid(self, source_id: int):
        with QtCore.QMutexLocker(_mutex):
            stmt = select(HistoryModel).where(HistoryModel.is_ignored == False, HistoryModel.wallpaper_source_id == source_id)
            for entry in self._session.scalars(stmt):
                entry.is_ignored = True
            self._session.commit()

    def get_sources(self, only_enabled=False):
        """
        Return a list of all the wallpaper sources.

        :param only_enabled: set to True if you only want the enabled sources.
        :return: a list of type WPSource of all the wallpaper sources.
        """
        with QtCore.QMutexLocker(_mutex):
            if only_enabled:
                stmt = select(WallpaperSourceModel).where(WallpaperSourceModel.enabled == True)
                return [x for x in self._session.scalars(stmt)]
            else:
                stmt = select(WallpaperSourceModel)
                return [x for x in self._session.scalars(stmt)]

    def add_source(self, source: WallpaperSourceModel):
        """
        Adds the given source to the database.

        :param source: the source to add.
        """
        with QtCore.QMutexLocker(_mutex):
            self._session.add(source)
            self._session.commit()

    def delete_source(self, source: WallpaperSourceModel):
        """
        Deletes the given source from the database.

        :param source: the source to delete
        """
        with QtCore.QMutexLocker(_mutex):
            self._session.delete(source)
            self._session.commit()

    def commit(self):
        """
        Commits any pending changes to the data.
        """
        with QtCore.QMutexLocker(_mutex):
            self._session.commit() # probably not the right way to do it
