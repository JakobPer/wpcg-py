# wpcg-py, a simple wallpaper changer
# Copyright (C) 2023  JakobPer
# 
# Full notice in Readme.md

class WallpaperSourceModel:
    """
    Defines a wallpaper source entry.
    """
    sid = -1
    url = ""
    enabled = True

    def __init__(self, sid, url, enabled=True):
        """
        Initializes the entry.

        :param sid: the id of the source entry
        :param url: the url of the source entry
        :param enabled: if the source should be enabled
        """
        self.sid = sid
        self.url = url
        self.enabled = enabled
