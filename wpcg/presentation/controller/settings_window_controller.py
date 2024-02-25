# wpcg-py, a simple wallpaper changer
# Copyright (C) 2023  JakobPer
# 
# Full notice in Readme.md

import logging

from PySide6.QtCore import QTime, Qt
from PySide6.QtWidgets import QMainWindow, QListWidgetItem, QFileDialog, QDialog, QMessageBox

from data.dao.config_dao import ConfigDAO
from data.dao.wallpaper_dao import WallpaperDAO
from data.model.wallpaper_source_model import WallpaperSourceModel
from presentation.controller.web_dialog_controller import WebDialogController
from presentation.ui.ui_settings import Ui_SettingsWindow

import platform
import os
import sys

if platform.system() == "Windows":
    import winreg


class SettingsWindowController(QMainWindow, Ui_SettingsWindow):
    """
    The Settings window using the gui from the ui file.
    """

    class SourceListWidgetItem(QListWidgetItem):
        """ ListWidgetItem for WPSources, so you can get the source object form a list item """

        def __init__(self, source: WallpaperSourceModel, *__args):
            """
            :param source: the WPSource object corresponding to this item
            :param __args: args for the super constructor
            """
            super().__init__(*__args)
            self.source = source

    config = None
    wpstore = None
    saved_callback = None
    selected = -1

    def __init__(self, config: ConfigDAO, wpstore: WallpaperDAO, saved_callback):
        """
        Initializes the Settings window.

        :param config: the config to load and save the settings from/to
        :param wpstore: the wpstore to manage the wp sources
        :param saved_callback: the callback to call after saving
        """
        super(SettingsWindowController, self).__init__()
        self.setupUi(self)

        self.config = config
        self.saved_callback = saved_callback

        self.lvSources.clear()
        # called when checkbox is changed
        self.lvSources.itemChanged.connect(self.listitem_changed)

        self.wpstore = wpstore
        # load sources
        wpsources = wpstore.get_sources()
        for source in wpsources:
            self.lvSources.addItem(self.create_list_item(source))

        # set event handler for buttons
        self.btnAddSource.pressed.connect(self.add_source)
        self.btnRemoveSource.pressed.connect(self.remove_pressed)
        self.btEditSource.pressed.connect(self.edit_pressed)
        self.btnWeb.pressed.connect(self.web_pressed)

        # bottom
        self.btnOk.pressed.connect(self.ok_pressed)

        # set config properties
        self.prettification_enabled = False
        self.repeat_background_enabled = False
        self.blur_background_enabled = False
        self.blend_edges_enabled = False
        self.wallpaper_width = 0
        self.wallpaper_height = 0
        self.blur_amount = 0.0
        self.blend_ratio = 0.0
        self.prettification_threshold = 0.0

        self.cb_enable_prettification.stateChanged.connect(self.cb_enable_prettification_clicked)
        self.cb_repeat_backround.stateChanged.connect(self.cb_repeat_backround_clicked)
        self.cb_blur_background.stateChanged.connect(self.cb_blur_background_clicked)
        self.cb_blend_edges.stateChanged.connect(self.cb_blend_edges_clicked)

        # windows tab
        windows_tab_index = self.tabWidget.indexOf(self.tab_windows)
        self.tabWidget.setTabVisible(windows_tab_index, platform.system() == "Windows")
        self.cb_autostart.stateChanged.connect(self.cb_autostart_windows_changed)
        # ToDo: re-enable once its working
        self.cb_autostart.setEnabled(False)

        self.reload_config()


    @staticmethod
    def create_list_item(source: WallpaperSourceModel):
        """
        Creates a list item based on a WPSource object.

        :param source: the WPSource to create the item for
        """
        item = SettingsWindowController.SourceListWidgetItem(source)
        item.setText(source.url)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(Qt.CheckState.Checked if source.enabled else Qt.CheckState.Unchecked)
        return item

    def closeEvent(self, event):
        """
        Called when the window tries to close. Just ignores the event and hides the window.
        """
        event.ignore()
        self.hide()

    def add_source(self):
        """Call to open a file dialog to add a new wallpaper source."""
        folder = QFileDialog.getExistingDirectory(parent=self, caption="Select wallpaper directory")
        if folder == "":
            return
        source = WallpaperSourceModel(-1, folder)
        self.lvSources.addItem(self.create_list_item(source))
        self.wpstore.add_source(source)

    def ok_pressed(self):
        """Called when ok is pressed. Saves the settings and calls the saved callback."""
        logging.debug("ok pressed")

        time = self.teInterval.time()
        interval = time.msecsSinceStartOfDay()
        self.config.set(ConfigDAO.KEY_INTERVAL, interval)
        self.config.set(ConfigDAO.KEY_PRETTIFICATION_ENABLED, str(self.cb_enable_prettification.isChecked()))
        self.config.set(ConfigDAO.KEY_REPEAT_BACKGROUND_ENABLED, str(self.cb_repeat_backround.isChecked()))
        self.config.set(ConfigDAO.KEY_BLUR_BACKGROUND_ENABLED, str(self.cb_blur_background.isChecked()))
        self.config.set(ConfigDAO.KEY_BLEND_EDGES_ENABLED, str(self.cb_blend_edges.isChecked()))
        self.config.set(ConfigDAO.KEY_WALLPAPER_WIDTH, self.sb_width.value())
        self.config.set(ConfigDAO.KEY_WALLPAPER_HEIGHT, self.sb_height.value())
        self.config.set(ConfigDAO.KEY_BLUR_AMOUNT, self.dsb_amount.value())
        self.config.set(ConfigDAO.KEY_BLEND_RATIO, self.dsb_blend_ratio.value())
        self.config.set(ConfigDAO.KEY_PRETTIFICATION_THRESHOLD, self.dsb_threshold.value())
        logging.debug("new interval: %d", interval)

        self.hide()
        self.saved_callback()


    def remove_pressed(self):
        """Called when the remove button is pressed. Removes the item from the list and from the WPStore."""
        selected = self.lvSources.selectedItems()
        if not selected:
            return

        for item in selected:
            source = item.source
            self.wpstore.delete_source(source)
            self.lvSources.takeItem(self.lvSources.row(item))

    def edit_pressed(self):
        """
        Called when the edit button is pressed. If an Item is selected, a file picker is opened and the item is
        changed in both the listView and the WPStore.
        """
        selected = self.lvSources.selectedItems()
        if not selected:
            return

        source = selected[0].source
        if source.url.startswith("http"):
            dialog = WebDialogController()
            dialog.leURL.setText(source.url)
            ret = dialog.exec()
            if ret == QDialog.DialogCode.Accepted:
                folder = dialog.leURL.text()
            else:
                return
        else:
            folder = QFileDialog.getExistingDirectory(parent=self, caption="Select wallpaper directory",
                                                      directory=source.url)
        if folder == "":
            return
        source.url = folder
        selected[0].setText(folder)
        self.wpstore.update_source(source)

    def listitem_changed(self, item: QListWidgetItem):
        """
        Called when a list item is changed. Updates the item int WPStore.
        :param item: the changed item
        """
        source = item.source
        source.enabled = item.checkState() == Qt.CheckState.Checked
        self.wpstore.update_source(source)

    def web_pressed(self):
        """
        Called when the web button is pressed. Shows a dialog to set the reddit URL.
        """
        dialog = WebDialogController()
        ret = dialog.exec()
        if ret == QDialog.DialogCode.Accepted:
            url = dialog.leURL.text()
            source = WallpaperSourceModel(-1, url)
            self.lvSources.addItem(self.create_list_item(source))
            self.wpstore.add_source(source)

    def show_error_message(self, text):
        """
        Show a error dialog with the given message.
        :param text: the text for the dialog
        """
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setText(text)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.show()

    def show(self):
        """Reloads the sources and Settings and then shows the window."""
        self.reload_config()

        super(SettingsWindowController, self).show()

    def reload_config(self):
        """
        Reloads the config and sets the ui values.
        """
        self.lvSources.clear()
        wpsources = self.wpstore.get_sources()
        for source in wpsources:
            self.lvSources.addItem(self.create_list_item(source))
        interval = int(self.config.get(ConfigDAO.KEY_INTERVAL, "0"))
        self.prettification_enabled = self.config.get(ConfigDAO.KEY_PRETTIFICATION_ENABLED, "False") == "True"
        self.repeat_background_enabled = self.config.get(ConfigDAO.KEY_REPEAT_BACKGROUND_ENABLED, "False") == "True"
        self.blur_background_enabled = self.config.get(ConfigDAO.KEY_BLUR_BACKGROUND_ENABLED, "False") == "True"
        self.blend_edges_enabled = self.config.get(ConfigDAO.KEY_BLEND_EDGES_ENABLED, "False") == "True"
        self.wallpaper_width = int(self.config.get(ConfigDAO.KEY_WALLPAPER_WIDTH))
        self.wallpaper_height = int(self.config.get(ConfigDAO.KEY_WALLPAPER_HEIGHT))
        self.blur_amount = float(self.config.get(ConfigDAO.KEY_BLUR_AMOUNT))
        self.blend_ratio = float(self.config.get(ConfigDAO.KEY_BLEND_RATIO))
        self.prettification_threshold = float(self.config.get(ConfigDAO.KEY_PRETTIFICATION_THRESHOLD))

        time = QTime(0, 0)
        time = time.addMSecs(interval)
        self.teInterval.setTime(time)

        self.cb_enable_prettification.setChecked(self.prettification_enabled)
        self.cb_repeat_backround.setChecked(self.repeat_background_enabled)
        self.cb_blur_background.setChecked(self.blur_background_enabled)
        self.cb_blend_edges.setChecked(self.blend_edges_enabled)

        self.dsb_threshold.setValue(self.prettification_threshold)
        self.sb_width.setValue(self.wallpaper_width)
        self.sb_height.setValue(self.wallpaper_height)
        self.dsb_amount.setValue(self.blur_amount)
        self.dsb_blend_ratio.setValue(self.blend_ratio)

        self.cb_autostart.setChecked(self.is_windows_autostart_enabled())

        self.reset_visibilities()

    def reset_visibilities(self):
        """
        Resets the visibilities of the groups in the wallpaper tab.
        """
        self.gb_prettification.setVisible(self.prettification_enabled)
        self.gb_repeat_settings.setVisible(self.repeat_background_enabled)
        self.gb_blur_settings.setVisible(self.blur_background_enabled)
        self.gb_blend_settings.setVisible(self.blend_edges_enabled)

    def cb_enable_prettification_clicked(self):
        self.prettification_enabled = self.cb_enable_prettification.isChecked()
        self.reset_visibilities()

    def cb_repeat_backround_clicked(self):
        self.repeat_background_enabled = self.cb_repeat_backround.isChecked()
        self.reset_visibilities()

    def cb_blur_background_clicked(self):
        self.blur_background_enabled = self.cb_blur_background.isChecked()
        self.reset_visibilities()

    def cb_blend_edges_clicked(self):
        self.blend_edges_enabled = self.cb_blend_edges.isChecked()
        self.reset_visibilities()

    def cb_autostart_windows_changed(self):
        pass # ToDo: implement without registry

    def is_windows_autostart_enabled(self):
        return False

