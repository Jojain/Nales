# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Projets\Nales\nales_alpha\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(971, 638)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.top_frame_container = QtWidgets.QWidget(self.centralwidget)
        self.top_frame_container.setObjectName("top_frame_container")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.top_frame_container)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.main_icons_container = QtWidgets.QWidget(self.top_frame_container)
        self.main_icons_container.setObjectName("main_icons_container")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.main_icons_container)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.pushButton = QtWidgets.QPushButton(self.main_icons_container)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_8.addWidget(self.pushButton)
        self.horizontalLayout_2.addWidget(self.main_icons_container)
        self.tabWidget = QtWidgets.QTabWidget(self.top_frame_container)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.horizontalLayout_2.addWidget(self.tabWidget)
        self.verticalLayout_3.addWidget(self.top_frame_container)
        self.center_app_container = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.center_app_container.sizePolicy().hasHeightForWidth())
        self.center_app_container.setSizePolicy(sizePolicy)
        self.center_app_container.setObjectName("center_app_container")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.center_app_container)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter_8 = QtWidgets.QSplitter(self.center_app_container)
        self.splitter_8.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_8.setObjectName("splitter_8")
        self.left_panel_container = QtWidgets.QWidget(self.splitter_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.left_panel_container.sizePolicy().hasHeightForWidth())
        self.left_panel_container.setSizePolicy(sizePolicy)
        self.left_panel_container.setObjectName("left_panel_container")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.left_panel_container)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.splitter = QtWidgets.QSplitter(self.left_panel_container)
        self.splitter.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(True)
        self.splitter.setObjectName("splitter")
        self.tree = QtWidgets.QTreeView(self.splitter)
        self.tree.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree.sizePolicy().hasHeightForWidth())
        self.tree.setSizePolicy(sizePolicy)
        self.tree.setMinimumSize(QtCore.QSize(0, 100))
        self.tree.setSizeIncrement(QtCore.QSize(1, 0))
        self.tree.setBaseSize(QtCore.QSize(200, 0))
        self.tree.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tree.setObjectName("tree")
        self.param_table_view = QtWidgets.QTableView(self.splitter)
        self.param_table_view.setObjectName("param_table_view")
        self.verticalLayout_5.addWidget(self.splitter)
        self.console_viewer_container = QtWidgets.QWidget(self.splitter_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.console_viewer_container.sizePolicy().hasHeightForWidth())
        self.console_viewer_container.setSizePolicy(sizePolicy)
        self.console_viewer_container.setObjectName("console_viewer_container")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.console_viewer_container)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter_3 = QtWidgets.QSplitter(self.console_viewer_container)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter_3.sizePolicy().hasHeightForWidth())
        self.splitter_3.setSizePolicy(sizePolicy)
        self.splitter_3.setOrientation(QtCore.Qt.Vertical)
        self.splitter_3.setObjectName("splitter_3")
        self.viewer = OCCTWidget(self.splitter_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.viewer.sizePolicy().hasHeightForWidth())
        self.viewer.setSizePolicy(sizePolicy)
        self.viewer.setMinimumSize(QtCore.QSize(0, 100))
        self.viewer.setSizeIncrement(QtCore.QSize(1, 0))
        self.viewer.setBaseSize(QtCore.QSize(800, 500))
        self.viewer.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.viewer.setObjectName("viewer")
        self.console_container = QtWidgets.QWidget(self.splitter_3)
        self.console_container.setObjectName("console_container")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.console_container)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self._console = ConsoleWidget(self.console_container)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._console.sizePolicy().hasHeightForWidth())
        self._console.setSizePolicy(sizePolicy)
        self._console.setMinimumSize(QtCore.QSize(0, 50))
        self._console.setObjectName("_console")
        self.verticalLayout_4.addWidget(self._console)
        self.verticalLayout.addWidget(self.splitter_3)
        self.verticalLayout_2.addWidget(self.splitter_8)
        self.verticalLayout_3.addWidget(self.center_app_container)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setEnabled(False)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 971, 20))
        self.menuBar.setDefaultUp(False)
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
from nales_alpha.widgets.console import ConsoleWidget
from nales_alpha.widgets.occt_widget import OCCTWidget
