#!/usr/bin/env bash

nuitka3 --standalone \
 --plugin-enable=pyside6 \
 --include-data-dir=wpcg/icons=icons \
 --disable-console \
 --company-name='github.com/JakobPer' \
 --product-name='wpcg' \
 --file-description='wpcg' \
 --file-version='1.0.0' \
 --linux-icon=wpcg/icons/icon.ico \
 ./wpcg/wpcg.py