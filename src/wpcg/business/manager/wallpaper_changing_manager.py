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
from pathlib import Path
from typing import Callable, List, Tuple
import requests

from wpcg.data.providers import provider
from wpcg.data.model.settings_model import SettingsModel
from wpcg.data.dao.wallpaper_dao import WallpaperDAO
from wpcg.utils import utils
from wpcg.utils.imageutils import ImageUtils

from PySide6.QtCore import QMutex, QMutexLocker, QObject, QRunnable, QThreadPool, QThread, Signal

# only import on windows
if platform.system() == "Windows":
    import ctypes

_mutex = QMutex()

class DownloadThread(QThread):

    progress = Signal(float)

    def __init__(self,provider_id: int, url: str, download_dir:str) -> None:
        super().__init__()
        self.url = url
        self.provider_id = provider_id
        self.download_dir = download_dir
        self.downloaded_file:str = None

    def run(self) -> None:
        if self.url.startswith('http'):
            try:
                logging.debug("Downloading {0}".format(self.url))
                self.downloaded_file = utils.download_file(self.url, self.download_dir, self.progress.emit)
                logging.debug("Downloading {0} finished".format(self.url))
            except Exception as e:
                logging.error("Failed to download {0}".format(self.url))
                logging.error(e)
        else: # It's a local file (ToDo make better handling than creating a thread for local files)
            self.downloaded_file = self.url


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
        self.download_queue : List[DownloadThread] = []
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
            self.download_queue.clear()
            self._predownload()

    def _predownload(self) -> None:
        if len(self.download_queue) < self.settings.predownload_count:
            nr = self.settings.predownload_count - len(self.download_queue)
            for _ in range(nr):
                (pid, wallpaper) = self._get_next_random()
                if wallpaper is not None:
                    thread = DownloadThread(pid, wallpaper, self.download_dir)
                    thread.start()
                    self.download_queue.append(thread)

    def _get_next_random(self) -> tuple[int, str]:
            rand = random.randrange(0, len(self.providers))
            return (rand, self.providers[rand].get_next())

    def next_wallpaper(self, progress: Callable[[float], None])-> bool:
        """
        Switches to the next wallpaper in the list of loaded wallpapers and removes it from the list. if the list is
        empty, set previouly shown wallpapers to ignore and load the wallpapers again.
        """
        if len(self.providers) == 0:
            return False

        with QMutexLocker(_mutex):
            if len(self.download_queue) == 0:
                self._predownload()

            thread = self.download_queue.pop(0)

            # wait for thread if running
            if thread.isRunning():
                logging.debug("waiting for download to finish...")
                thread.progress.connect(progress)
                thread.wait()

            self._predownload() # fill queue again immediatelly so download starts as early as possible

            wallpaper = thread.downloaded_file

            if wallpaper is None:
                return False

            self.prev_counter = 1
            self._set_wallpaper(wallpaper)
            self.wpstore.add_history_entry(wallpaper, self.providers[thread.provider_id].source.sid)

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
