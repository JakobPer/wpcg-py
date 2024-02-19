# wpcg-py, a simple wallpaper changer
# Copyright (C) 2023  JakobPer
# 
# Full notice in Readme.md

import urllib.request

from urllib3.util.url import *

from business.manager.wallpaper_changing_manager import *
from data.dao.wallpaper_dao import WallpaperDAO
from typing import List

from data.model.wallpaper_source_model import WallpaperSourceModel
import requests


class Provider:

    def __init__(self, source: WallpaperSourceModel, wpstore: WallpaperDAO, download_dir: string):
        self.source = source
        self.wpstore = wpstore
        self.download_dir = download_dir

    def reload(self):
        pass

    def get_next(self) -> string:
        return ""

    @staticmethod
    def is_image(img: string):
        """
        Checks file name if it ends in known image endings. (jpg, jpeg, png, bmp, gif)

        :param img: the image filename
        :return: true if it is a known image format, false otherwise.
        """
        i = img.lower()
        return i.endswith('jpg') or i.endswith('jpeg') or i.endswith('png') or i.endswith('bmp') or i.endswith('gif')


class FileProvider(Provider):

    def __init__(self, source: WallpaperSourceModel, wpstore: WallpaperDAO, download_dir: string):

        super().__init__(source, wpstore, download_dir)
        self.wplist = []

    def reload(self):
        wpdir = self.source.url

        if not os.path.isdir(wpdir):
            logging.warning("could not find wallpaper directory: %s" % wpdir)
            return

        for root, dirs, files in os.walk(wpdir):
            for f in files:
                file = os.path.join(root, f)
                if self.is_image(file):
                    self.wplist.append(file)

        shown = self.wpstore.get_all()
        for s in shown:
            if self.wplist.__contains__(s):
                self.wplist.remove(s)

        random.shuffle(self.wplist)

    def get_next(self) -> string:
        if len(self.wplist) == 0:
            logging.debug("used all wallpapers, reloading")
            self.wpstore.ignore_all_by_sourceid(self.source.sid)
            self.reload()
            if len(self.wplist) == 0:  # we really did not find any
                logging.warning("no usable wallpapers found")
                return

        target = self.wplist[0]
        self.wplist.remove(target)

        if not os.path.isfile(target):
            return None

        return target

class ZeroChanProvider(Provider):

    def __init__(self, source: WallpaperSourceModel, wpstore: WallpaperDAO, download_dir: string):
        super().__init__(source, wpstore, download_dir)
        self.wplist = []

    def reload(self):
        self.wplist = []

        split = urlsplit(self.source.url)
        url = urlunsplit((
            split[0],
            split[1],
            split[2],
            (split[3] if 'json' in split[3] else split[3]+'&json') + '&l=250',
            split[4],
        ))

        logging.debug("Parsing zerochan url: %s", url)
        # get zerochan json
        try:
            r = requests.get(url, headers={'User-agent': 'wpcg test'})
            json = r.json()
            for elem in json['items']:
                id = elem['id']
                self.wplist.append(id)
        except Exception as e:
            logging.error("Could not get zerochan page %s", url)
            logging.error(str(e))

        shown = self.wpstore.get_all()
        for s in shown:
            if s in self.wplist:
                self.wplist.remove(s)

        random.shuffle(self.wplist)

    def get_next(self) -> string:
        if len(self.wplist) == 0:
            logging.debug("used all wallpapers, reloading")
            self.wpstore.ignore_all_by_sourceid(self.source.sid)
            self.reload()
            if len(self.wplist) == 0:  # we really did not find any
                logging.warning("no usable wallpapers found")
                return
        
        id = self.wplist.pop()
        url = "https://zerochan.net/" + str(id) +"?json"

        try:
            r = requests.get(url, headers={'User-agent': 'wpcg test'} )
            json = r.json()
            url = json['full']
            target = os.path.join(self.download_dir,unquote(url.split('/')[-1]))
            if not os.path.exists(target):
                logging.debug("Downloading: %s", url)
                urllib.request.urlretrieve(url, target)
                logging.debug("downloaded to: " + target)
            else:
                logging.debug("already downloaded")

        except Exception as e:
            logging.error("Could not get zerochan page %s", url)
            logging.error(str(e))

        if not os.path.isfile(target):
            return None

        return target


def get_providers(sources: List[WallpaperSourceModel], wp_dao: WallpaperDAO, wallpaper_dir: string) \
        -> List[Provider]:
    providers = []
    for source in sources:
        if 'zerochan' in source.url:
            providers.append(ZeroChanProvider(source, wp_dao, wallpaper_dir))
        else:
            providers.append(FileProvider(source, wp_dao, wallpaper_dir))
    return providers
