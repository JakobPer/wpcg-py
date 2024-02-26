# wpcg-py, a simple wallpaper changer
# Copyright (C) 2023  JakobPer
# 
# Full notice in Readme.md

from pathlib import Path

def get_app_dir():
    """
    :return: The absolute path to the app directory as a string.
    """
    userdir = Path.home()
    app_dir = userdir.joinpath(".wpcg")
    if not app_dir.exists():
        app_dir.mkdir()

    return str(app_dir)


def get_download_dir():
    """
    :return: The absolute path to the app download directory.
    """
    app_dir = Path(get_app_dir())
    download_dir = app_dir.joinpath("downloaded")
    if not download_dir.exists():
        download_dir.mkdir()

    return str(download_dir)

def get_prettified_dir():
    """
    :return: The absolute path to the app download directory.
    """
    download_dir = Path(get_download_dir())
    prettified_dir = download_dir.joinpath('prettified')
    if not prettified_dir.exists():
        prettified_dir.mkdir()

    return str(prettified_dir)


