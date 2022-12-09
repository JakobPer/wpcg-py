import logging
import os
import sys

from PyQt6.QtWidgets import QApplication
import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtGui import QIcon

from presentation.controller import main_controller
from utils import utils


class AppContext:  # 1. Subclass ApplicationContext

    logging.basicConfig(level=logging.DEBUG, filename=os.path.join(utils.get_app_dir(), 'wpcg.log'), filemode='w',
                        format='%(name)s - %(levelname)s - %(message)s')

    w = None

    def run(self):  # 2. Implement run()
        app = QApplication(sys.argv)
        icon = QIcon('icons/icon.ico')
        if len(icon.availableSizes()) == 0:
            print("Could not find icon")
            exit(-1)
        icon_loading = QIcon('icons/icon_loading.ico')
        if len(icon_loading.availableSizes()) == 0:
            print("Could not find loading icon")
            exit(-1)
        self.w = main_controller.MainController(app, icon, icon_loading)
        return app.exec() # 3. End run() with this line


if __name__ == '__main__':
    appctxt = AppContext()  # 4. Instantiate the subclass
    exit_code = appctxt.run()  # 5. Invoke run()
    sys.exit(exit_code)
