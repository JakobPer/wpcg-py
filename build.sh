#!/usr/bin/env bash

#./build-ui.sh

pyinstaller --clean -y --noconsole -p wpcg -i ./wpcg/icons/Icon.ico --add-data "wpcg/icons:icons" ./wpcg/wpcg.py
