# wpcg-py, a simple wallpaper changer
# Copyright (C) 2023  JakobPer
# 
# Full notice in Readme.md

from PySide6.QtWidgets import QDialog

from presentation.ui import ui_webDialog


class WebDialogController(QDialog, ui_webDialog.Ui_Dialog):
    """
    Implementation for the Web select Dialog.
    """

    def __init__(self):
        """
        Initializes the dialog.
        """
        super().__init__()
        self.setupUi(self)
