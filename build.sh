#!/usr/bin/env bash

#./build-ui.sh

pyinstaller --clean --onedir -y --noconsole -p wpcg -i ./wpcg/icons/Icon.ico --add-data "wpcg/icons:icons" --contents-directory "." ./wpcg/wpcg.py
