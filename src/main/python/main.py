import logging
import os
import sys

from fbs_runtime.application_context.PyQt5 import ApplicationContext

from presentation.controller import main_controller
from utils import utils


class AppContext(ApplicationContext):  # 1. Subclass ApplicationContext
    """
    Application Context used by fbs. For more info check the fbs docs.
    """
    logging.basicConfig(level=logging.DEBUG, filename=os.path.join(utils.get_app_dir(), 'wpcg.log'), filemode='w',
                        format='%(name)s - %(levelname)s - %(message)s')

    w = None

    def run(self):  # 2. Implement run()
        """run method of the fbs app."""
        self.w = main_controller.MainController(self.app, self.app_icon)
        return self.app.exec_()  # 3. End run() with this line


if __name__ == '__main__':
    appctxt = AppContext()  # 4. Instantiate the subclass
    exit_code = appctxt.run()  # 5. Invoke run()
    sys.exit(exit_code)
