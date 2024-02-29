# wpcg-py, a simple wallpaper changer
# Copyright (C) 2023  JakobPer
# 
# Full notice in Readme.md

import logging

from PySide6.QtCore import QThread, QTimer, QEvent, Qt, QRunnable,QThreadPool, Signal, QObject
from PySide6.QtGui import QIcon, QAction, QPixmap
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication

from business.manager.wallpaper_changing_manager import WallpaperChangingManager
from data.dao.settings_dao import SettingsDAO
from presentation.controller.settings_window_controller import SettingsWindowController

from presentation.ui import icon_resources_rc
import math

class MainController:
    """
    Wallpaper Changer main class. Handles TrayIcon creation and Settings.
    """

    class ChangeThread (QThread):
        succeeded = Signal(None)
        failed = Signal(None)
        progress = Signal(float)

        def __init__(self, changer: WallpaperChangingManager) -> None:
            super().__init__()

            self.changer = changer

    class NextWallpaperThread(ChangeThread):

        def run(self) -> None:
            if self.changer is not None:
                if self.changer.next_wallpaper(self.progress.emit):
                    self.succeeded.emit()
                else:
                    self.failed.emit()
            else:
                self.failed.emit()

    class PreviousWallpaperThread(ChangeThread):

        def run(self) -> None:
            if self.changer is not None:
                if self.changer.previous_wallpaper():
                    self.succeeded.emit()
                else:
                    self.failed.emit()
            else:
                self.failed.emit()

    class ReloadWallpaperThread(ChangeThread):

        def run(self) -> None:
            if self.changer is not None:
                self.changer.reload_wallpaper_list()
            self.succeeded.emit()

    def __init__(self, app: QApplication):
        """
        Initializes the Wallpaperchanger. Loads settings and wallpapers. Creates TrayIcon and Settings.

        :param app: the QT app
        :param icon: the app icon
        """

        self.app = app
        self.settings_dao = SettingsDAO()
        self.settings = self.settings_dao.load()

        QThreadPool.globalInstance().setMaxThreadCount(4)

        self.wplist = []
        # timer that changes the wallpaper
        self.timer = QTimer()

        logging.debug("using interval of %d ms", self.settings.change_interval)

        # create the changer
        self.changer = WallpaperChangingManager(self.settings)
        self.next_thread: MainController.NextWallpaperThread = None
        self.previous_thread: MainController.PreviousWallpaperThread = None
        self.reload_thread: MainController.ReloadWallpaperThread = None

        # init settings window
        self.settings_window = SettingsWindowController(self.settings_dao, self.changer.wpstore, self._settings_saved)

        # create tray icon
        self.icon = QIcon(u":icons/icons/icon.ico")
        self.loading_icon = QIcon(u":icons/icons/icon_loading.ico")
        self.progress_icons = [QIcon(u":icons/icons/progress_{}.ico".format(i)) for i in range(1,25)]
        self.progress_icon_index = -1

        self.trayicon = QSystemTrayIcon()
        self.trayicon.setIcon(self.icon)
        self.trayicon.activated.connect(self._activated)  # icon double click
        self.trayicon.event = self._trayEvent

        # context menu actions of the icon
        settingsIcon = QIcon()
        settingsIconName=u"settings-configure"
        if QIcon.hasThemeIcon(settingsIconName):
            settingsIcon = QIcon.fromTheme(settingsIconName)
        else:
            settingsIcon.addPixmap(QPixmap(':icons/icons/ic_fluent_settings_24_filled.svg'), QIcon.Mode.Normal, QIcon.State.Off)
        self.settings_action = QAction(settingsIcon, "Settings")
        self.settings_action.triggered.connect(self.show_settings)

        nextIcon = QIcon()
        nextIconName = u"arrow-right"
        if QIcon.hasThemeIcon(nextIconName):
            nextIcon = QIcon.fromTheme(nextIconName)
        else:
            nextIcon.addPixmap(QPixmap(':icons/icons/ic_fluent_arrow_right_24_filled.svg'), QIcon.Mode.Normal, QIcon.State.Off)
        self.next_action = QAction(nextIcon, "Next wallpaper")
        self.next_action.triggered.connect(self._context_next)

        prevIcon = QIcon()
        prevIconName = u"arrow-left"
        if QIcon.hasThemeIcon(prevIconName):
            prevIcon = QIcon.fromTheme(prevIconName)
        else:
            prevIcon.addPixmap(QPixmap(':icons/icons/ic_fluent_arrow_left_24_filled.svg'), QIcon.Mode.Normal, QIcon.State.Off)
        self.prev_action = QAction(prevIcon, "Previous wallpaper")
        self.prev_action.triggered.connect(self._context_previous)

        exitIcon = QIcon()
        exitIconName = u"application-exit"
        if QIcon.hasThemeIcon(exitIconName):
            exitIcon = QIcon.fromTheme(exitIconName)
            self.exit_action = QAction(exitIcon, "Exit")
        else:
            self.exit_action = QAction("Exit")
        self.exit_action.triggered.connect(self.close)

        # create the context menu
        self.menu = QMenu()
        self.menu.addAction(self.next_action)
        self.menu.addAction(self.prev_action)
        self.menu.addAction(self.settings_action)
        self.menu.addAction(self.exit_action)
        self.trayicon.setContextMenu(self.menu)

        self._reset_tooltip()

        # show it
        self.trayicon.show()
        self.trayicon.setVisible(True)

        # start the timer
        self.timer.timeout.connect(self._context_next)
        self.timer.start(self.settings.change_interval)

    def _trayEvent(self, ev: QEvent):
        if ev.type() == QEvent.Type.Wheel:
            self._context_next()
            return True

        return False

    def action_in_progress(self):
        return self.next_thread is not None and self.next_thread.isRunning() or \
            self.previous_thread is not None and self.previous_thread.isRunning() or \
            self.reload_thread is not None and self.reload_thread.isRunning()

    def _reset_tooltip(self):
        self.trayicon.setToolTip("Click for next wallpaper")

    def _start_loading(self):
        self.trayicon.setIcon(self.loading_icon)
        self.trayicon.setToolTip("Setting wallpaper...")

    def _stop_loading(self):
        self.trayicon.setIcon(self.icon)
        self.progress_icon_index = -1
        self._reset_tooltip()

    def _context_next(self):
        """shows next wallpaper."""
        if self.next_thread is not None and self.next_thread.isRunning():
            self.next_thread.requestInterruption()
            self.next_thread.wait()
        elif self.action_in_progress():
            logging.debug("Action in progress, aborting")
            return

        self._start_loading()
        self.settings_action.setEnabled(False)
        self.next_thread = MainController.NextWallpaperThread(self.changer)
        self.next_thread.succeeded.connect(self._action_completed)
        self.next_thread.failed.connect(self._action_failed)
        self.next_thread.progress.connect(self._action_progress)
        self._start_thread(self.next_thread)
        self.timer.stop()
        self.timer.start(self.settings.change_interval)

    def _context_previous(self):
        """shows the previous wallpaper."""
        if self.previous_thread is not None and self.previous_thread.isRunning():
            self.previous_thread.requestInterruption()
            self.previous_thread.wait()
        elif self.action_in_progress():
            logging.debug("Action in progress, aborting")
            return

        self._start_loading()
        self.settings_action.setEnabled(False)
        self.previous_thread = MainController.PreviousWallpaperThread(self.changer)
        self.previous_thread.succeeded.connect(self._action_completed)
        self.previous_thread.failed.connect(self._action_failed)
        self._start_thread(self.previous_thread)
        self.timer.stop()
        self.timer.start(self.settings.change_interval)

    def _action_completed(self):
        self.settings_action.setEnabled(True)
        if not self.action_in_progress():
            self._stop_loading()

    def _action_failed(self):
        self.trayicon.showMessage("Failed to set wallpaper", "try again...", QSystemTrayIcon.MessageIcon.Critical)
        self._action_completed()

    def _action_progress(self, progress: float):
        p = 0.0 if progress < 0 else progress
        p = 1.0 if p > 1 else p
        self.trayicon.setToolTip("Downloading image {0}%".format(int(p*100)))
        i = math.floor(p * (len(self.progress_icons)-1))
        icon = self.progress_icons[i]
        if self.progress_icon_index != i:
            self.progress_icon_index = i
            self.trayicon.setIcon(icon)

    def _activated(self, reason):
        """called when the icon is double clicked to change to next wallpaper."""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self._context_next()

    def close(self):
        """the close event. Hide the icon (else it stays in the taskbar) and stop everything."""
        self.trayicon.hide()
        self.timer.stop()
        self.app.quit()

    def show_settings(self):
        """Shows the settings window."""
        self.settings_window.show()

    def _settings_saved(self):
        """called after the settings are saved. Reloads the wallpapers and restarts the timer."""
        logging.debug("Settings saved")
        self.settings = self.settings_dao.load()
        self.changer.settings = self.settings

        self.reload_thread = MainController.ReloadWallpaperThread(self.changer)
        self.reload_thread.succeeded.connect(self._action_completed)
        self._start_thread(self.reload_thread)
        self.timer.stop()
        self.timer.start(self.settings.change_interval)

    def _start_thread(self, thread: QThread):
        #QThreadPool.globalInstance().start(thread)
        thread.start()

