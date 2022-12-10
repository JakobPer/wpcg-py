#!/usr/bin/env bash

./build-ui.sh

pyinstaller -y --noconsole -i ./src/main/python/icons/Icon.ico --add-data "src/main/python/icons;icons" ./src/main/python/wpcg.py