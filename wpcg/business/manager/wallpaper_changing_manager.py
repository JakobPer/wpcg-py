# wpcg-py, a simple wallpaper changer
# Copyright (C) 2023  JakobPer
# 
# Full notice in Readme.md

import logging
import os
import platform
import random
import string
import urllib
from subprocess import call
from urllib.parse import *
from data.providers import provider
from pathlib import Path

import requests

# only import on windows
from data.dao.config_dao import ConfigDAO
from data.dao.wallpaper_dao import WallpaperDAO
from utils import utils
from utils.imageutils import ImageUtils
from PySide6 import QtCore

if platform.system() == "Windows":
    import ctypes

_mutex = QtCore.QMutex()


class WallpaperChangingManager:
    """
    Handles loading, managing, and switching of wallpapers.
    """
    prev_counter = 1
    wpstore = None

    def __init__(self, config: ConfigDAO):
        """Initializes the wallpaper changer. Loads all wallpapers."""
        self.config = config
        self.prev_counter = 1
        self.wpstore = WallpaperDAO()
        self.download_dir = utils.get_download_dir()
        self.prettified_dir = utils.get_prettified_dir()
        self.providers = []
        self.reload_wallpaper_list()

    def reload_wallpaper_list(self):
        """
        Reloads all the wallpapers defined in the sources. Looks in each folder recursively to find all images therein.
        Then removes all the wallpapers that where already shown to the user. At last shuffles the list to make it
        random.
        """
        with QtCore.QMutexLocker(_mutex):
            wpsources = self.wpstore.get_sources(only_enabled=True)
            self.providers = provider.get_providers(wpsources, self.wpstore, self.download_dir)
            for prov in self.providers:
                prov.reload()

    def next_wallpaper(self, thread: QtCore.QThread):
        """
        Switches to the next wallpaper in the list of loaded wallpapers and removes it from the list. if the list is
        empty, set previouly shown wallpapers to ignore and load the wallpapers again.
        """
        if len(self.providers) == 0:
            return

        with QtCore.QMutexLocker(_mutex):
            rand = random.randrange(0, len(self.providers))
            wallpaper = self.providers[rand].get_next()

            # ToDo: proper error handling
            if wallpaper is None:
                return

            self.prev_counter = 1
            self._set_wallpaper(wallpaper, thread)
            self.wpstore.add_history_entry(wallpaper, self.providers[rand].source.sid)

            logging.debug("set wallpaper to: %s" % wallpaper)

    def previous_wallpaper(self, thread: QtCore.QThread):
        """
        Set the wallpaper to the previously shown one.
        """

        with QtCore.QMutexLocker(_mutex):
            url = self.wpstore.get_previous(self.prev_counter)
            if url is None:
                return

            self.prev_counter = self.prev_counter + 1

            target = url

            if not os.path.isfile(target):
                self.previous_wallpaper()

            self._set_wallpaper(target, thread)
            logging.debug("set to previous wallpaper to: %s", target)

    def _set_wallpaper(self, image: string, thread: QtCore.QThread):
        """
        Sets the wallpaper to the given image. Sets it depending on the platform it is running on.

        :param image: the full path to the image
        """

        prettification_enabled = self.config.get(ConfigDAO.KEY_PRETTIFICATION_ENABLED) == "True"

        im = image
        # already set image before it was prettified as preview
        # self._set_wallpaper_platform(im)

        if thread.isInterruptionRequested(): return

        if prettification_enabled:
            threshold = float(self.config.get(ConfigDAO.KEY_PRETTIFICATION_THRESHOLD))
            repeat_background_enabled = self.config.get(ConfigDAO.KEY_REPEAT_BACKGROUND_ENABLED) == "True"
            blur_background_enabled = self.config.get(ConfigDAO.KEY_BLUR_BACKGROUND_ENABLED) == "True"
            blend_edges_enabled = self.config.get(ConfigDAO.KEY_BLEND_EDGES_ENABLED) == "True"
            wallpaper_width = int(self.config.get(ConfigDAO.KEY_WALLPAPER_WIDTH))
            wallpaper_height = int(self.config.get(ConfigDAO.KEY_WALLPAPER_HEIGHT))
            blur_amount = float(self.config.get(ConfigDAO.KEY_BLUR_AMOUNT))
            blend_ratio = float(self.config.get(ConfigDAO.KEY_BLEND_RATIO))
            try:
                format = 'jpeg'
                imname = Path(im).name
                imname = os.path.splitext(imname)[0]+'.'+format
                target = os.path.join(self.prettified_dir, imname)
                if ImageUtils.make_pretty(image, target, repeat_background=repeat_background_enabled,
                                          blend_edges=blend_edges_enabled, blur_background=blur_background_enabled,
                                          width=wallpaper_width, height=wallpaper_height, sigma=blur_amount,
                                          blend_ratio=blend_ratio, thresh=threshold, format=format, quality=95):
                    logging.debug("wallpaper prettified")
                    im = target
                else:
                    logging.debug("prettification not needed")
            except Exception as e:
                logging.error("Could not prettyfy wallpaper!", exc_info=True)

        self._set_wallpaper_for_platform(im)


    def _set_wallpaper_for_platform(self, image: string):
        """
        Sets the wallpaper for the correct target platform

        :param image: path to the image
        """
        if platform.system() == "Linux":
            #self._set_wallpaper_gnome(image)
            filepath = os.path.abspath(image)
            self._set_wallpaper_kde(filepath)
        elif platform.system() == "Windows":
            self._set_wallpaper_windows(image)
        else:
            logging.error("Could not detect OS type!")
            logging.error("Only supporting Linux(Gnome3) and Windows. Detected: %s" % platform.system())

    def _set_wallpaper_kde(self, image):

        call(['plasma-apply-wallpaperimage', image])

        return True

    def _set_wallpaper_gnome(self, image_file_with_path):
        """
        Sets the wallpaper for gnome like desktop environments. Basically just calls gsettings.

        :param image_file_with_path: the full path to the image
        """
        filepath = os.path.abspath(image_file_with_path)

        # works on Gnome3
        call(['/usr/bin/gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', 'file://%s' % filepath])
        call(['/usr/bin/gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri-dark', 'file://%s' % filepath])

        return True

    def _set_wallpaper_windows(self, image_file_with_path):
        """
        Sets the wallpaper on windows.

        :param image_file_with_path: the full path to the image
        """

        filepath = os.path.abspath(image_file_with_path)

        ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath, 3)

        return True
