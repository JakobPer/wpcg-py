# wpcg-py, a simple wallpaper changer
# Copyright (C) 2023  JakobPer
# 
# Full notice in Readme.md

import logging
import os
import sys

from PyQt6.QtWidgets import QApplication
import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtGui import QIcon
import PyQt6.QtCore as QtCore

from presentation.controller import main_controller
from utils import utils

import icons.rc_icon_resources


class AppContext:  # 1. Subclass ApplicationContext

    logging.basicConfig(level=logging.DEBUG, filename=os.path.join(utils.get_app_dir(), 'wpcg.log'), filemode='w',
                        format='%(name)s - %(levelname)s - %(message)s')

    w = None

    def run(self):  # 2. Implement run()
        cwd = os.path.join(os.getcwd(), os.path.dirname(sys.argv[0]))
        QtCore.QDir.addSearchPath('icons', os.path.join(cwd, 'icons'))
        app = QApplication(sys.argv)
        icon = QIcon(os.path.join(cwd, 'icons/icon.ico'))
        icon_loading = QIcon(os.path.join(cwd,'icons/icon_loading.ico'))
        self.w = main_controller.MainController(app, icon, icon_loading)
        return app.exec() # 3. End run() with this line


if __name__ == '__main__':
    appctxt = AppContext()  # 4. Instantiate the subclass
    exit_code = appctxt.run()  # 5. Invoke run()
    sys.exit(exit_code)
