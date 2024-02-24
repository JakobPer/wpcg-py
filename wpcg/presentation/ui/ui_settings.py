# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLayout,
    QListWidget, QListWidgetItem, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QTabWidget,
    QTimeEdit, QVBoxLayout, QWidget)
from . import icon_resources_rc

class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        if not SettingsWindow.objectName():
            SettingsWindow.setObjectName(u"SettingsWindow")
        SettingsWindow.resize(752, 602)
        icon = QIcon()
        icon.addFile(u":/icons/icons/icon.ico", QSize(), QIcon.Normal, QIcon.On)
        SettingsWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(SettingsWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_general = QWidget()
        self.tab_general.setObjectName(u"tab_general")
        self.verticalLayout_3 = QVBoxLayout(self.tab_general)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.tab_general)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lvSources = QListWidget(self.tab_general)
        self.lvSources.setObjectName(u"lvSources")

        self.horizontalLayout_3.addWidget(self.lvSources)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.btnAddSource = QPushButton(self.tab_general)
        self.btnAddSource.setObjectName(u"btnAddSource")
        self.btnAddSource.setMaximumSize(QSize(50, 16777215))
        self.btnAddSource.setBaseSize(QSize(0, 0))
        icon1 = QIcon()
        iconThemeName = u"folder-new"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u":/icons/icons/ic_fluent_add_24_filled.svg", QSize(), QIcon.Normal, QIcon.On)

        self.btnAddSource.setIcon(icon1)

        self.verticalLayout_2.addWidget(self.btnAddSource)

        self.btnRemoveSource = QPushButton(self.tab_general)
        self.btnRemoveSource.setObjectName(u"btnRemoveSource")
        self.btnRemoveSource.setMaximumSize(QSize(50, 16777215))
        self.btnRemoveSource.setBaseSize(QSize(0, 0))
        icon2 = QIcon()
        iconThemeName = u"delete"
        if QIcon.hasThemeIcon(iconThemeName):
            icon2 = QIcon.fromTheme(iconThemeName)
        else:
            icon2.addFile(u":/icons/icons/ic_fluent_delete_24_filled.svg", QSize(), QIcon.Normal, QIcon.Off)

        self.btnRemoveSource.setIcon(icon2)

        self.verticalLayout_2.addWidget(self.btnRemoveSource)

        self.btEditSource = QPushButton(self.tab_general)
        self.btEditSource.setObjectName(u"btEditSource")
        self.btEditSource.setMaximumSize(QSize(50, 16777215))
        self.btEditSource.setBaseSize(QSize(0, 0))
        icon3 = QIcon()
        iconThemeName = u"document-edit"
        if QIcon.hasThemeIcon(iconThemeName):
            icon3 = QIcon.fromTheme(iconThemeName)
        else:
            icon3.addFile(u":/icons/icons/ic_fluent_edit_24_filled.svg", QSize(), QIcon.Normal, QIcon.Off)

        self.btEditSource.setIcon(icon3)

        self.verticalLayout_2.addWidget(self.btEditSource)

        self.btnWeb = QPushButton(self.tab_general)
        self.btnWeb.setObjectName(u"btnWeb")
        self.btnWeb.setMaximumSize(QSize(50, 16777215))
        icon4 = QIcon()
        iconThemeName = u"link"
        if QIcon.hasThemeIcon(iconThemeName):
            icon4 = QIcon.fromTheme(iconThemeName)
        else:
            icon4.addFile(u":/icons/icons/ic_fluent_link_24_filled.svg", QSize(), QIcon.Normal, QIcon.Off)
            icon4.addFile(u":/icons/icons/ic_fluent_link_24_filled.svg", QSize(), QIcon.Normal, QIcon.On)

        self.btnWeb.setIcon(icon4)

        self.verticalLayout_2.addWidget(self.btnWeb)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.teInterval = QTimeEdit(self.tab_general)
        self.teInterval.setObjectName(u"teInterval")
        self.teInterval.setMinimumSize(QSize(60, 0))

        self.gridLayout.addWidget(self.teInterval, 0, 3, 1, 1)

        self.label_2 = QLabel(self.tab_general)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout)

        self.tabWidget.addTab(self.tab_general, "")
        self.tab_wallpaper = QWidget()
        self.tab_wallpaper.setObjectName(u"tab_wallpaper")
        self.verticalLayout_4 = QVBoxLayout(self.tab_wallpaper)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.cb_enable_prettification = QCheckBox(self.tab_wallpaper)
        self.cb_enable_prettification.setObjectName(u"cb_enable_prettification")

        self.verticalLayout_4.addWidget(self.cb_enable_prettification)

        self.gb_prettification = QGroupBox(self.tab_wallpaper)
        self.gb_prettification.setObjectName(u"gb_prettification")
        self.verticalLayout = QVBoxLayout(self.gb_prettification)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_8 = QLabel(self.gb_prettification)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_4.addWidget(self.label_8)

        self.dsb_threshold = QDoubleSpinBox(self.gb_prettification)
        self.dsb_threshold.setObjectName(u"dsb_threshold")
        self.dsb_threshold.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_4.addWidget(self.dsb_threshold)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.groupBox_3 = QGroupBox(self.gb_prettification)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_2 = QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_7 = QLabel(self.groupBox_3)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 1, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 0, 2, 1, 1)

        self.label_6 = QLabel(self.groupBox_3)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)

        self.sb_width = QSpinBox(self.groupBox_3)
        self.sb_width.setObjectName(u"sb_width")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.sb_width.sizePolicy().hasHeightForWidth())
        self.sb_width.setSizePolicy(sizePolicy2)
        self.sb_width.setMinimumSize(QSize(80, 0))
        self.sb_width.setMaximum(20000)
        self.sb_width.setValue(1920)

        self.gridLayout_2.addWidget(self.sb_width, 0, 1, 1, 1)

        self.sb_height = QSpinBox(self.groupBox_3)
        self.sb_height.setObjectName(u"sb_height")
        sizePolicy2.setHeightForWidth(self.sb_height.sizePolicy().hasHeightForWidth())
        self.sb_height.setSizePolicy(sizePolicy2)
        self.sb_height.setMinimumSize(QSize(80, 0))
        self.sb_height.setMaximum(20000)
        self.sb_height.setValue(1080)

        self.gridLayout_2.addWidget(self.sb_height, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.cb_repeat_backround = QCheckBox(self.gb_prettification)
        self.cb_repeat_backround.setObjectName(u"cb_repeat_backround")

        self.verticalLayout.addWidget(self.cb_repeat_backround)

        self.gb_repeat_settings = QGroupBox(self.gb_prettification)
        self.gb_repeat_settings.setObjectName(u"gb_repeat_settings")
        self.verticalLayout_5 = QVBoxLayout(self.gb_repeat_settings)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.cb_blur_background = QCheckBox(self.gb_repeat_settings)
        self.cb_blur_background.setObjectName(u"cb_blur_background")

        self.verticalLayout_5.addWidget(self.cb_blur_background)

        self.gb_blur_settings = QGroupBox(self.gb_repeat_settings)
        self.gb_blur_settings.setObjectName(u"gb_blur_settings")
        self.verticalLayout_6 = QVBoxLayout(self.gb_blur_settings)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_4 = QLabel(self.gb_blur_settings)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.dsb_amount = QDoubleSpinBox(self.gb_blur_settings)
        self.dsb_amount.setObjectName(u"dsb_amount")
        self.dsb_amount.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_2.addWidget(self.dsb_amount)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.cb_blend_edges = QCheckBox(self.gb_blur_settings)
        self.cb_blend_edges.setObjectName(u"cb_blend_edges")

        self.verticalLayout_6.addWidget(self.cb_blend_edges)

        self.gb_blend_settings = QGroupBox(self.gb_blur_settings)
        self.gb_blend_settings.setObjectName(u"gb_blend_settings")
        self.gridLayout_5 = QGridLayout(self.gb_blend_settings)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_5 = QLabel(self.gb_blend_settings)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_5.addWidget(self.label_5, 0, 0, 1, 1)

        self.dsb_blend_ratio = QDoubleSpinBox(self.gb_blend_settings)
        self.dsb_blend_ratio.setObjectName(u"dsb_blend_ratio")
        self.dsb_blend_ratio.setMinimumSize(QSize(80, 0))

        self.gridLayout_5.addWidget(self.dsb_blend_ratio, 0, 1, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_5, 0, 2, 1, 1)


        self.verticalLayout_6.addWidget(self.gb_blend_settings)


        self.verticalLayout_5.addWidget(self.gb_blur_settings)


        self.verticalLayout.addWidget(self.gb_repeat_settings)


        self.verticalLayout_4.addWidget(self.gb_prettification)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.tab_wallpaper, "")
        self.tab_windows = QWidget()
        self.tab_windows.setObjectName(u"tab_windows")
        self.verticalLayout_8 = QVBoxLayout(self.tab_windows)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.cb_autostart = QCheckBox(self.tab_windows)
        self.cb_autostart.setObjectName(u"cb_autostart")

        self.verticalLayout_8.addWidget(self.cb_autostart)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_3)

        self.tabWidget.addTab(self.tab_windows, "")

        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btnOk = QPushButton(self.centralwidget)
        self.btnOk.setObjectName(u"btnOk")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.btnOk.sizePolicy().hasHeightForWidth())
        self.btnOk.setSizePolicy(sizePolicy3)

        self.horizontalLayout.addWidget(self.btnOk)


        self.gridLayout_3.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        SettingsWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SettingsWindow)

        self.tabWidget.setCurrentIndex(0)
        self.btnOk.setDefault(True)


        QMetaObject.connectSlotsByName(SettingsWindow)
    # setupUi

    def retranslateUi(self, SettingsWindow):
        SettingsWindow.setWindowTitle(QCoreApplication.translate("SettingsWindow", u"Settings", None))
        self.label.setText(QCoreApplication.translate("SettingsWindow", u"Wallpaper Sources:", None))
        self.btnAddSource.setText("")
        self.btnRemoveSource.setText("")
        self.btEditSource.setText("")
        self.btnWeb.setText("")
        self.label_2.setText(QCoreApplication.translate("SettingsWindow", u"Interval (hh:mm):", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_general), QCoreApplication.translate("SettingsWindow", u"General", None))
#if QT_CONFIG(tooltip)
        self.cb_enable_prettification.setToolTip(QCoreApplication.translate("SettingsWindow", u"<html><head/><body><p>If prettification is\n"
"                                          enabled, a new wallpaper will be generated where the source image will be put\n"
"                                          into its center. Unless repeat image in background is checked, the background\n"
"                                          will be filled with the median edge color of the central image.</p><p><span\n"
"                                          style=\" font-weight:600;\">Be aware that this option will cost\n"
"                                          some performance while the wallpaper gets generated and it will slow down\n"
"                                          wallpaper changing.</span></p></body></html>\n"
"                                      ", None))
#endif // QT_CONFIG(tooltip)
        self.cb_enable_prettification.setText(QCoreApplication.translate("SettingsWindow", u"Enable prettification", None))
        self.gb_prettification.setTitle(QCoreApplication.translate("SettingsWindow", u"Prettification settings", None))
        self.label_8.setText(QCoreApplication.translate("SettingsWindow", u"Prettification threshold:", None))
#if QT_CONFIG(tooltip)
        self.dsb_threshold.setToolTip(QCoreApplication.translate("SettingsWindow", u"<html><head/><body><p>Prettification\n"
"                                                              is only applied if the source image ratio and definded\n"
"                                                              width/height ratio difference exceedes this threshold.\n"
"                                                              Lower values mean the ratio has to be more similar, bigger\n"
"                                                              values mean the ratios can deviate more.</p></body></html>\n"
"                                                          ", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_3.setTitle(QCoreApplication.translate("SettingsWindow", u"Wallpaper size", None))
        self.label_7.setText(QCoreApplication.translate("SettingsWindow", u"Height:", None))
        self.label_6.setText(QCoreApplication.translate("SettingsWindow", u"Width:", None))
#if QT_CONFIG(tooltip)
        self.sb_width.setToolTip(QCoreApplication.translate("SettingsWindow", u"The resulting width of the generated wallpaper.\n"
"                                                              ", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.sb_height.setToolTip(QCoreApplication.translate("SettingsWindow", u"The resulting height of the generated wallpaper.\n"
"                                                              ", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.cb_repeat_backround.setToolTip(QCoreApplication.translate("SettingsWindow", u"<html><head/><body><p>If repeat image\n"
"                                                      in background is checked, the source image will be repeated in the\n"
"                                                      background instead of the median color. A gaussian blur can also\n"
"                                                      be applied only to the images in the background if checked.</p></body></html>\n"
"                                                  ", None))
#endif // QT_CONFIG(tooltip)
        self.cb_repeat_backround.setText(QCoreApplication.translate("SettingsWindow", u"Repeat image in background", None))
        self.gb_repeat_settings.setTitle(QCoreApplication.translate("SettingsWindow", u"Repeat settings", None))
#if QT_CONFIG(tooltip)
        self.cb_blur_background.setToolTip(QCoreApplication.translate("SettingsWindow", u"<html><head/><body><p>If\n"
"                                                                  blur background is selected, a gaussian blur is\n"
"                                                                  applied to the background before the central image is\n"
"                                                                  composited in.</p></body></html>\n"
"                                                              ", None))
#endif // QT_CONFIG(tooltip)
        self.cb_blur_background.setText(QCoreApplication.translate("SettingsWindow", u"Blur background", None))
        self.gb_blur_settings.setTitle(QCoreApplication.translate("SettingsWindow", u"Blur settings", None))
        self.label_4.setText(QCoreApplication.translate("SettingsWindow", u"Amount:", None))
#if QT_CONFIG(tooltip)
        self.dsb_amount.setToolTip(QCoreApplication.translate("SettingsWindow", u"The amount of blur that should\n"
"                                                                                      be applied.\n"
"                                                                                  ", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.cb_blend_edges.setToolTip(QCoreApplication.translate("SettingsWindow", u"<html><head/><body><p>If\n"
"                                                                              blend edges is checked, the edges of the\n"
"                                                                              central image are blended with the\n"
"                                                                              background to get a smoother transition.</p></body></html>\n"
"                                                                          ", None))
#endif // QT_CONFIG(tooltip)
        self.cb_blend_edges.setText(QCoreApplication.translate("SettingsWindow", u"Blend edges with background", None))
        self.gb_blend_settings.setTitle(QCoreApplication.translate("SettingsWindow", u"Blend Settings", None))
        self.label_5.setText(QCoreApplication.translate("SettingsWindow", u"Blend ratio:", None))
#if QT_CONFIG(tooltip)
        self.dsb_blend_ratio.setToolTip(QCoreApplication.translate("SettingsWindow", u"how many percent of the\n"
"                                                                                          central image should be\n"
"                                                                                          blurred. (0=0%, 1=100%)\n"
"                                                                                      ", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_wallpaper), QCoreApplication.translate("SettingsWindow", u"Wallpaper", None))
        self.cb_autostart.setText(QCoreApplication.translate("SettingsWindow", u"Autostart", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_windows), QCoreApplication.translate("SettingsWindow", u"Windows", None))
        self.btnOk.setText(QCoreApplication.translate("SettingsWindow", u"Ok", None))
    # retranslateUi

