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
from typing import Callable

import requests

# only import on windows
from data.model.settings_model import SettingsModel
from data.dao.wallpaper_dao import WallpaperDAO
from utils import utils
from utils.imageutils import ImageUtils
from PySide6.QtCore import QMutex, QMutexLocker, QRunnable, QThreadPool, QThread, Signal

if platform.system() == "Windows":
    import ctypes

_mutex = QMutex()


class WallpaperChangingManager:
    """
    Handles loading, managing, and switching of wallpapers.
    """

    def __init__(self, settings: SettingsModel):
        """Initializes the wallpaper changer. Loads all wallpapers."""
        self.settings = settings
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
        with QMutexLocker(_mutex):
            wpsources = self.wpstore.get_sources(only_enabled=True)
            self.providers = provider.get_providers(wpsources, self.wpstore, self.download_dir)
            for prov in self.providers:
                prov.reload()

    def _download_file(self, url: str, download_dir:str, progress: Callable[[float], None]) -> str:
        progress(0)

        target = os.path.join(self.download_dir,unquote(url.split('/')[-1]))
        if not os.path.exists(target):
            logging.debug("Downloading: %s", url)
            with open(target, "wb") as f:
                response = requests.get(url, stream=True)
                total = response.headers.get('content-length')
                if total is None: # no content length, write whole file
                    logging.debug("Could not get content length, download all")
                    f.write(response.content)
                else:
                    loaded = 0
                    total = int(total)
                    for data in response.iter_content(chunk_size=4096):
                        logging.debug("Download progress {0}/{1}".format(loaded, total))
                        loaded += len(data)
                        f.write(data)
                        if progress is not None:
                            percent = loaded/total
                            progress(percent)

            logging.debug("downloaded to: " + target)
        else:
            logging.debug("already downloaded")
        
        progress(100)

        return target if os.path.exists(target) else None


    def next_wallpaper(self, progress: Callable[[float], None])-> bool:
        """
        Switches to the next wallpaper in the list of loaded wallpapers and removes it from the list. if the list is
        empty, set previouly shown wallpapers to ignore and load the wallpapers again.
        """
        if len(self.providers) == 0:
            return

        with QMutexLocker(_mutex):
            rand = random.randrange(0, len(self.providers))
            wallpaper = self.providers[rand].get_next()

            if wallpaper.startswith('http'):
                wallpaper = self._download_file(wallpaper, self.download_dir, progress)

            if wallpaper is None:
                return False

            self.prev_counter = 1
            self._set_wallpaper(wallpaper)
            self.wpstore.add_history_entry(wallpaper, self.providers[rand].source.sid)

            logging.debug("set wallpaper to: %s" % wallpaper)

            return True

    def previous_wallpaper(self) -> bool:
        """
        Set the wallpaper to the previously shown one.
        """

        with QMutexLocker(_mutex):
            url = self.wpstore.get_previous(self.prev_counter)
            if url is None:
                return False

            self.prev_counter = self.prev_counter + 1

            target = url

            if not os.path.isfile(target):
                self.previous_wallpaper()

            self._set_wallpaper(target)
            logging.debug("set to previous wallpaper to: %s", target)

            return True

    def _set_wallpaper(self, image: string):
        """
        Sets the wallpaper to the given image. Sets it depending on the platform it is running on.

        :param image: the full path to the image
        """

        prettification_enabled = self.settings.prettification_enabled

        im = image
        # already set image before it was prettified as preview
        # self._set_wallpaper_platform(im)

        if QThread.currentThread().isInterruptionRequested(): return

        if prettification_enabled:
            threshold = self.settings.prettification_threshold
            repeat_background_enabled = self.settings.repeat_background
            blur_background_enabled = self.settings.blur_background
            blend_edges_enabled = self.settings.blend_edges
            wallpaper_width = self.settings.wallpaper_width
            wallpaper_height = self.settings.wallpaper_height
            blur_amount = self.settings.blur_amount
            blend_ratio = self.settings.blend_ratio
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

        if QThread.currentThread().isInterruptionRequested(): return

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
