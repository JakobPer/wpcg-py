import logging
import os
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from presentation.controller import main_controller
from utils import utils


class AppContext:  # 1. Subclass ApplicationContext

    logging.basicConfig(level=logging.DEBUG, filename=os.path.join(utils.get_app_dir(), 'wpcg.log'), filemode='w',
                        format='%(name)s - %(levelname)s - %(message)s')

    w = None

    def run(self):  # 2. Implement run()
        app = QApplication(sys.argv)
        icon = QIcon('icons/icon.ico')
        self.w = main_controller.MainController(app, icon)
        return app.exec_()  # 3. End run() with this line


if __name__ == '__main__':
    appctxt = AppContext()  # 4. Instantiate the subclass
    exit_code = appctxt.run()  # 5. Invoke run()
    sys.exit(exit_code)
