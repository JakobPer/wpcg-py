# wpcg-py, a simple wallpaper changer
# Copyright (C) 2023  JakobPer
# 
# Full notice in Readme.md

import logging
import os
import sys

from PySide6.QtWidgets import QApplication
import PySide6.QtWidgets as QtWidgets
from PySide6.QtGui import QIcon
import PySide6.QtCore as QtCore
# import QtSvg cause otherwise Svg resources don't work on Win11 for some reason... 
from PySide6 import QtSvg, QtXml # DO NOT REMOVE

from presentation.controller import main_controller
from utils import utils


class AppContext:  # 1. Subclass ApplicationContext

    logging.basicConfig(level=logging.DEBUG, filename=os.path.join(utils.get_app_dir(), 'wpcg.log'), filemode='w',
                        format='%(name)s - %(levelname)s - %(message)s')

    w = None

    def run(self):  # 2. Implement run()
        app = QApplication(sys.argv)
        self.w = main_controller.MainController(app)
        return app.exec() # 3. End run() with this line


if __name__ == '__main__':
    appctxt = AppContext()  # 4. Instantiate the subclass
    exit_code = appctxt.run()  # 5. Invoke run()
    sys.exit(exit_code)
