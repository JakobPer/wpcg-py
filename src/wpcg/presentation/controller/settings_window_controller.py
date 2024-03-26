# wpcg-py, a simple wallpaper changer
# Copyright (C) 2023  JakobPer
# 
# Full notice in Readme.md

import logging

from PySide6.QtCore import QTime, Qt
from PySide6.QtWidgets import QMainWindow, QListWidgetItem, QFileDialog, QDialog, QMessageBox

from wpcg.data.dao.settings_dao import SettingsDAO, AppSettingsModel
from wpcg.data.dao.wallpaper_dao import WallpaperDAO
from wpcg.data.model.wallpaper_source_model import WallpaperSourceModel
from wpcg.presentation.controller.web_dialog_controller import WebDialogController
from wpcg.presentation.ui.ui_settings import Ui_SettingsWindow

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

    def __init__(self, settings_dao: SettingsDAO, wpstore: WallpaperDAO, saved_callback):
        """
        Initializes the Settings window.

        :param config: the config to load and save the settings from/to
        :param wpstore: the wpstore to manage the wp sources
        :param saved_callback: the callback to call after saving
        """
        super(SettingsWindowController, self).__init__()
        self.setupUi(self)

        self.selected = -1

        self.settings_dao = settings_dao
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

        self.leAppDir.textChanged.connect(self.app_dir_changed)
        self.leDownloadDir.textChanged.connect(self.download_dir_changed)
        self.lePrettifyDir.textChanged.connect(self.prettify_dir_changed)

        self.btPickAppDir.pressed.connect(self.set_app_dir)
        self.btPickDownloadDir.pressed.connect(self.set_download_dir)
        self.btPickPrettifyDir.pressed.connect(self.set_prettify_dir)

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
        self.settings.change_interval = interval
        self.settings.predownload_count = self.sbPredownloadCount.value()
        self.settings.prettification_enabled = self.cb_enable_prettification.isChecked()
        self.settings.repeat_background = self.cb_repeat_backround.isChecked()
        self.settings.blur_background = self.cb_blur_background.isChecked()
        self.settings.blend_edges = self.cb_blend_edges.isChecked()
        self.settings.wallpaper_width = self.sb_width.value()
        self.settings.wallpaper_height = self.sb_height.value()
        self.settings.blur_amount = self.dsb_amount.value()
        self.settings.blend_ratio = self.dsb_blend_ratio.value()
        self.settings.prettification_threshold = self.dsb_threshold.value()

        self.appsettings.base_dir = self.leAppDir.text()
        self.appsettings.download_dir = self.leDownloadDir.text()
        self.appsettings.prettify_dir = self.lePrettifyDir.text()

        self.settings_dao.save_app_settings(self.appsettings)
        self.settings_dao.save_shared(self.settings, self.appsettings)

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

        self.appsettings = self.settings_dao.load_app_settings()
        self.settings = self.settings_dao.load_shared(self.appsettings)

        # reload wallpaper list
        self.lvSources.clear()
        wpsources = self.wpstore.get_sources()
        for source in wpsources:
            self.lvSources.addItem(self.create_list_item(source))

        time = QTime(0, 0)
        time = time.addMSecs(self.settings.change_interval)
        self.teInterval.setTime(time)
        self.sbPredownloadCount.setValue(self.settings.predownload_count)
        self.leAppDir.setText(self.appsettings.base_dir)
        self.leDownloadDir.setText(self.appsettings.download_dir)
        self.lePrettifyDir.setText(self.appsettings.prettify_dir)

        self.cb_enable_prettification.setChecked(self.settings.prettification_enabled)
        self.cb_repeat_backround.setChecked(self.settings.repeat_background)
        self.cb_blur_background.setChecked(self.settings.blur_background)
        self.cb_blend_edges.setChecked(self.settings.blend_edges)

        self.dsb_threshold.setValue(self.settings.prettification_threshold)
        self.sb_width.setValue(self.settings.wallpaper_width)
        self.sb_height.setValue(self.settings.wallpaper_height)
        self.dsb_amount.setValue(self.settings.blur_amount)
        self.dsb_blend_ratio.setValue(self.settings.blend_ratio)


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

    def app_dir_changed(self):
        dir = self.leAppDir.text()
        if not os.path.exists(dir):
            self.show_error_message("App directory could not be found!")
            self.leAppDir.setText(self.appsettings.base_dir)

    def download_dir_changed(self):
        dir = self.leDownloadDir.text()
        if not os.path.exists(dir):
            self.show_error_message("Download directory could not be found!")
            self.leDownloadDir.setText(self.appsettings.download_dir)

    def prettify_dir_changed(self):
        dir = self.lePrettifyDir.text()
        if not os.path.exists(dir):
            self.show_error_message("Prettify directory could not be found!")
            self.lePrettifyDir.setText(self.appsettings.prettify_dir)

    def set_app_dir(self):
        folder = QFileDialog.getExistingDirectory(parent=self, caption="Select wpcg main directory")
        if folder == "":
            return
        self.leAppDir.setText(folder)

        answer = QMessageBox.question(self, "Update other directories?", "Also update download and prettify directory to be in this directory?", QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)

        if answer == QMessageBox.StandardButton.Yes:
            tmp = AppSettingsModel(folder)
            self.leDownloadDir.setText(tmp.download_dir)
            self.lePrettifyDir.setText(tmp.prettify_dir)

    def set_download_dir(self):
        folder = QFileDialog.getExistingDirectory(parent=self, caption="Select wallpaper download directory")
        if folder == "":
            return
        self.leDownloadDir.setText(folder)

    def set_prettify_dir(self):
        folder = QFileDialog.getExistingDirectory(parent=self, caption="Select where prettified wallpapers stored")
        if folder == "":
            return
        self.lePrettifyDir.setText(folder)

