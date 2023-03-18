# wpcg-py, a simple wallpaper changer
# Copyright (C) 2023  JakobPer
# 
# Full notice in Readme.md

import logging

from PySide6.QtCore import QThread, QTimer, QEvent, Qt
from PySide6.QtGui import QIcon, QAction, QPixmap
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication

from business.manager.wallpaper_changing_manager import WallpaperChangingManager
from data.dao.config_dao import ConfigDAO
from presentation.controller.settings_window_controller import SettingsWindowController

from presentation.ui import icon_resources_rc

class MainController:
    """
    Wallpaper Changer main class. Handles TrayIcon creation and Settings.
    """

    class NextWallpaperThread(QThread):

        def __init__(self, changer: WallpaperChangingManager):
            QThread.__init__(self)
            self.changer = changer

        def __del__(self):
            self.wait()

        def run(self):
            if self.changer is not None:
                self.changer.next_wallpaper(self)

    class PreviousWallpaperThread(QThread):

        def __init__(self, changer: WallpaperChangingManager):
            QThread.__init__(self)
            self.changer = changer

        def __del__(self):
            self.wait()

        def run(self):
            if self.changer is not None:
                self.changer.previous_wallpaper(self)

    class ReloadWallpaperThread(QThread):

        def __init__(self, changer: WallpaperChangingManager):
            QThread.__init__(self)
            self.changer = changer

        def __del__(self):
            self.wait()

        def run(self):
            if self.changer is not None:
                self.changer.reload_wallpaper_list()

    def __init__(self, app: QApplication, icon: QIcon, loadingIcon: QIcon):
        """
        Initializes the Wallpaperchanger. Loads settings and wallpapers. Creates TrayIcon and Settings.

        :param app: the QT app
        :param icon: the app icon
        """

        self.app = app
        self.config = ConfigDAO()

        # set default config parameters
        self.set_default_config()

        self.wplist = []
        # timer that changes the wallpaper
        self.timer = QTimer()
        self.interval = int(self.config.get(ConfigDAO.KEY_INTERVAL))

        logging.debug("using interval of %d ms", self.interval)

        # create the changer
        self.changer = WallpaperChangingManager(self.config)
        self.next_thread = MainController.NextWallpaperThread(self.changer)
        self.next_thread.finished.connect(self.action_completed)
        self.previous_thread = MainController.PreviousWallpaperThread(self.changer)
        self.previous_thread.finished.connect(self.action_completed)
        self.reload_thread = MainController.ReloadWallpaperThread(self.changer)
        self.reload_thread.finished.connect(self.action_completed)
        # init settings window
        self.settings_window = SettingsWindowController(self.config, self.changer.wpstore, self.settings_saved)

        # create tray icon
        self.icon = icon
        self.loading_icon = loadingIcon
        self.trayicon = QSystemTrayIcon()
        self.trayicon.setIcon(icon)
        self.trayicon.activated.connect(self.activated)  # icon double click
        self.trayicon.event = self.trayEvent

        # context menu actions of the icon
        settingsIcon = QIcon()
        settingsIcon.addPixmap(QPixmap(':icons/icons/ic_fluent_settings_24_filled.svg'), QIcon.Mode.Normal, QIcon.State.Off)
        self.settings_action = QAction(settingsIcon, "Settings")
        self.settings_action.triggered.connect(self.show_settings)

        nextIcon = QIcon()
        nextIcon.addPixmap(QPixmap(':icons/icons/ic_fluent_arrow_right_24_filled.svg'), QIcon.Mode.Normal, QIcon.State.Off)
        self.next_action = QAction(nextIcon, "Next wallpaper")
        self.next_action.triggered.connect(self.context_next)

        prevIcon = QIcon()
        prevIcon.addPixmap(QPixmap(':icons/icons/ic_fluent_arrow_left_24_filled.svg'), QIcon.Mode.Normal, QIcon.State.Off)
        self.prev_action = QAction(prevIcon, "Previous wallpaper")
        self.prev_action.triggered.connect(self.context_previous)

        self.exit_action = QAction("Exit")
        self.exit_action.triggered.connect(self.close)

        # create the context menu
        self.menu = QMenu()
        self.menu.addAction(self.next_action)
        self.menu.addAction(self.prev_action)
        self.menu.addAction(self.settings_action)
        self.menu.addAction(self.exit_action)
        self.trayicon.setContextMenu(self.menu)

        # show it
        self.trayicon.show()
        self.trayicon.setVisible(True)

        # start the timer
        self.timer.timeout.connect(self.context_next)
        self.timer.start(self.interval)

    def set_default_config(self):
        if not self.config.contains_key(ConfigDAO.KEY_INTERVAL):
            self.config.set(ConfigDAO.KEY_INTERVAL, 3600000)
        if not self.config.contains_key(ConfigDAO.KEY_PRETTIFICATION_THRESHOLD):
            self.config.set(ConfigDAO.KEY_PRETTIFICATION_THRESHOLD, 0.1)
        if not self.config.contains_key(ConfigDAO.KEY_PRETTIFICATION_ENABLED):
            self.config.set(ConfigDAO.KEY_PRETTIFICATION_ENABLED, str(True))
        if not self.config.contains_key(ConfigDAO.KEY_REPEAT_BACKGROUND_ENABLED):
            self.config.set(ConfigDAO.KEY_REPEAT_BACKGROUND_ENABLED, str(True))
        if not self.config.contains_key(ConfigDAO.KEY_BLUR_BACKGROUND_ENABLED):
            self.config.set(ConfigDAO.KEY_BLUR_BACKGROUND_ENABLED, str(True))
        if not self.config.contains_key(ConfigDAO.KEY_BLEND_EDGES_ENABLED):
            self.config.set(ConfigDAO.KEY_BLEND_EDGES_ENABLED, str(True))
        if not self.config.contains_key(ConfigDAO.KEY_WALLPAPER_WIDTH):
            self.config.set(ConfigDAO.KEY_WALLPAPER_WIDTH, 1920)
        if not self.config.contains_key(ConfigDAO.KEY_WALLPAPER_HEIGHT):
            self.config.set(ConfigDAO.KEY_WALLPAPER_HEIGHT, 1080)
        if not self.config.contains_key(ConfigDAO.KEY_BLUR_AMOUNT):
            self.config.set(ConfigDAO.KEY_BLUR_AMOUNT, 10)
        if not self.config.contains_key(ConfigDAO.KEY_BLEND_RATIO):
            self.config.set(ConfigDAO.KEY_BLEND_RATIO, 0.02)

    def trayEvent(self, ev: QEvent):
        if ev.type() == QEvent.Type.Wheel:
            self.context_next()
            return True

        return False

    def action_in_progress(self):
        return self.next_thread.isRunning() or self.previous_thread.isRunning() or self.reload_thread.isRunning()

    def start_loading(self):
        self.trayicon.setIcon(self.loading_icon)

    def stop_loading(self):
        self.trayicon.setIcon(self.icon)

    def context_next(self):
        """shows next wallpaper."""
        if self.next_thread.isRunning():
            self.next_thread.requestInterruption()
            self.next_thread.wait()
            self.next_thread = MainController.NextWallpaperThread(self.changer)
            self.next_thread.finished.connect(self.action_completed)
        elif self.action_in_progress():
            logging.debug("Action in progress, aborting")
            return

        self.start_loading()
        self.settings_action.setEnabled(False)
        self.next_thread.start()
        self.timer.stop()
        self.timer.start(self.interval)

    def context_previous(self):
        """shows the previous wallpaper."""
        if self.previous_thread.isRunning():
            self.previous_thread.requestInterruption()
            self.previous_thread.wait()
            self.previous_thread = MainController.PreviousWallpaperThread(self.changer)
            self.previous_thread.finished.connect(self.action_completed)
        elif self.action_in_progress():
            logging.debug("Action in progress, aborting")
            return

        self.start_loading()
        self.settings_action.setEnabled(False)
        self.previous_thread.start()
        self.timer.stop()
        self.timer.start(self.interval)

    def action_completed(self):
        self.settings_action.setEnabled(True)
        if not self.action_in_progress():
            self.stop_loading()

    def activated(self, reason):
        """called when the icon is double clicked to change to next wallpaper."""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.context_next()

    def close(self):
        """the close event. Hide the icon (else it stays in the taskbar) and stop everything."""
        self.trayicon.hide()
        self.timer.stop()
        self.app.quit()

    def show_settings(self):
        """Shows the settings window."""
        self.settings_window.show()

    def settings_saved(self):
        """called after the settings are saved. Reloads the wallpapers and restarts the timer."""
        logging.debug("Settings saved")
        self.reload_thread.start()
        self.interval = int(self.config.get(ConfigDAO.KEY_INTERVAL))
        self.timer.stop()
        self.timer.start(self.interval)
