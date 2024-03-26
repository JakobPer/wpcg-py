# wpcg-py, a simple wallpaper changer
# Copyright (C) 2023  JakobPer
# 
# Full notice in Readme.md

from pathlib import Path
import logging
import os
from typing import Callable
import requests
from urllib.parse import unquote


def get_app_dir():
    """
    :return: The absolute path to the app directory as a string.
    """
    userdir = Path.home()
    app_dir = userdir.joinpath(".wpcg")
    if not app_dir.exists():
        app_dir.mkdir()

    return str(app_dir)


def get_download_dir(app_dir: str):
    """
    :return: The absolute path to the app download directory.
    """
    app_dir = Path(app_dir)
    download_dir = app_dir.joinpath("downloaded")
    if not download_dir.exists():
        download_dir.mkdir()

    return str(download_dir)

def get_prettified_dir(download_dir: str):
    """
    :return: The absolute path to the app download directory.
    """
    download_dir = Path(download_dir)
    prettified_dir = download_dir.joinpath('prettified')
    if not prettified_dir.exists():
        prettified_dir.mkdir()

    return str(prettified_dir)

def download_file(url: str, download_dir:str, progress: Callable[[float], None]) -> str:
    progress(0)

    target = os.path.join(download_dir, unquote(url.split('/')[-1]))
    if not os.path.exists(target):
        with open(target, "wb") as f:
            response = requests.get(url, stream=True)
            total = response.headers.get('content-length')
            if total is None: # no content length, write whole file
                f.write(response.content)
            else:
                loaded = 0
                total = int(total)
                for data in response.iter_content(chunk_size=4096):
                    loaded += len(data)
                    f.write(data)
                    if progress is not None:
                        percent = loaded/total
                        progress(percent)
    
    progress(100)

    return target if os.path.exists(target) else None
