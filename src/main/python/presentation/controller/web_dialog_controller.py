from PyQt6.QtWidgets import QDialog

from presentation.ui import webDialog


class WebDialogController(QDialog, webDialog.Ui_Dialog):
    """
    Implementation for the Web select Dialog.
    """

    def __init__(self):
        """
        Initializes the dialog.
        """
        super(QDialog, self).__init__()
        self.setupUi(self)
