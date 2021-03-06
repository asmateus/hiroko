# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design/hiroko.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
from pyqtgraph import PlotWidget
import pyqtgraph as pg


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        pg.setConfigOption('background', (236, 237, 238))
        pg.setConfigOption('foreground', 'k')

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 650)
        MainWindow.setMinimumSize(QtCore.QSize(1300, 730))
        MainWindow.setMaximumSize(QtCore.QSize(1300, 730))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.option_holder = QtWidgets.QGroupBox(self.centralwidget)
        self.option_holder.setGeometry(QtCore.QRect(20, 0, 381, 121))
        self.option_holder.setTitle("")
        self.option_holder.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.option_holder.setObjectName("option_holder")
        self.start_btn = QtWidgets.QPushButton(self.option_holder)
        self.start_btn.setGeometry(QtCore.QRect(20, 70, 88, 34))
        self.start_btn.setObjectName("start_btn")
        self.previous_btn = QtWidgets.QPushButton(self.option_holder)
        self.previous_btn.setGeometry(QtCore.QRect(130, 70, 51, 34))
        self.previous_btn.setObjectName("previous_btn")
        self.next_btn = QtWidgets.QPushButton(self.option_holder)
        self.next_btn.setGeometry(QtCore.QRect(130, 30, 51, 34))
        self.next_btn.setObjectName("next_btn")
        self.day_count = QtWidgets.QSpinBox(self.option_holder)
        self.day_count.setGeometry(QtCore.QRect(20, 30, 88, 34))
        self.day_count.setReadOnly(False)
        self.day_count.setMinimum(10)
        self.day_count.setMaximum(20)
        self.day_count.setProperty("value", 10)
        self.day_count.setObjectName("day_count")
        self.deviation_info = QtWidgets.QLabel(self.option_holder)
        self.deviation_info.setGeometry(QtCore.QRect(200, 60, 171, 18))
        self.deviation_info.setObjectName("deviation_info")
        self.distance_info = QtWidgets.QLabel(self.option_holder)
        self.distance_info.setGeometry(QtCore.QRect(200, 40, 171, 18))
        self.distance_info.setObjectName("distance_info")
        self.fitness_info = QtWidgets.QLabel(self.option_holder)
        self.fitness_info.setGeometry(QtCore.QRect(200, 80, 171, 18))
        self.fitness_info.setObjectName("fitness_info")
        self.epoch_counter = QtWidgets.QLabel(self.centralwidget)
        self.epoch_counter.setGeometry(QtCore.QRect(580, 100, 160, 25))
        self.epoch_counter.setObjectName("epoch_counter")
        self.map_holder = QtWidgets.QGroupBox(self.centralwidget)
        self.map_holder.setGeometry(QtCore.QRect(750, 50, 524, 594))
        self.map_holder.setTitle("")
        self.map_holder.setObjectName("map_holder")
        self.map_holder_label = QtWidgets.QLabel(self.map_holder)
        self.map_holder_label.setGeometry(QtCore.QRect(0, 0, 524, 594))
        self.map_holder_label.setObjectName("map_holder_label")
        self.scatter_plot = PlotWidget(self.centralwidget)
        self.scatter_plot.setGeometry(QtCore.QRect(20, 130, 701, 271))
        self.scatter_plot.setObjectName("scatter_plot")
        self.bar_plot = PlotWidget(self.centralwidget)
        self.bar_plot.setGeometry(QtCore.QRect(20, 400, 701, 271))
        self.bar_plot.setObjectName("bar_plot")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 30))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuNew = QtWidgets.QMenu(self.menuFile)
        self.menuNew.setObjectName("menuNew")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionGenetic = QtWidgets.QAction(MainWindow)
        self.actionGenetic.setObjectName("actionGenetic")
        self.actionRandom = QtWidgets.QAction(MainWindow)
        self.actionRandom.setObjectName("actionRandom")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionModify = QtWidgets.QAction(MainWindow)
        self.actionModify.setObjectName("actionModify")
        self.actionImport_Rule_Book = QtWidgets.QAction(MainWindow)
        self.actionImport_Rule_Book.setObjectName("actionImport_Rule_Book")
        self.menuNew.addAction(self.actionGenetic)
        self.menuNew.addAction(self.actionRandom)
        self.menuFile.addAction(self.menuNew.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuSettings.addAction(self.actionModify)
        self.menuSettings.addAction(self.actionImport_Rule_Book)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.start_btn.setText(_translate("MainWindow", "Start"))
        self.previous_btn.setText(_translate("MainWindow", "Prev"))
        self.next_btn.setText(_translate("MainWindow", "Next"))
        self.deviation_info.setText(_translate("MainWindow", "Best Deviation:"))
        self.distance_info.setText(_translate("MainWindow", "Best Distance:"))
        self.fitness_info.setText(_translate("MainWindow", "Fitness Value:"))
        self.epoch_counter.setText(_translate("MainWindow", "Epochs: 0  Idle: 0"))
        self.map_holder_label.setText(_translate("MainWindow", "Map"))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le"))
        self.menuNew.setTitle(_translate("MainWindow", "&New"))
        self.menuSettings.setTitle(_translate("MainWindow", "&Settings"))
        self.actionGenetic.setText(_translate("MainWindow", "&Genetic"))
        self.actionRandom.setText(_translate("MainWindow", "&Random"))
        self.actionOpen.setText(_translate("MainWindow", "&Load dump File"))
        self.actionModify.setText(_translate("MainWindow", "&Modify"))
        self.actionImport_Rule_Book.setText(_translate("MainWindow", "&Import Rule Book"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
