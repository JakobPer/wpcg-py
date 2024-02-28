#!/usr/bin/env bash

nuitka3 --standalone \
 --onefile \
 --plugin-enable=pyside6 \
 --disable-console \
 --output-dir=build \
 --company-name='github.com/JakobPer' \
 --product-name='wpcg' \
 --file-description='wpcg' \
 --file-version='1.0.0' \
 --linux-icon=src/wpcg/icons/linux/1024.png \
 ./src/wpcg/wpcg.py