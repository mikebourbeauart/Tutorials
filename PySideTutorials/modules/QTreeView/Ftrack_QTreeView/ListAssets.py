# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ListAssets.ui'
#
# Created: Fri Apr 12 13:54:31 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ListAssets(object):
    def setupUi(self, ListAssets):
        ListAssets.setObjectName("ListAssets")
        ListAssets.resize(558, 412)
        self.horizontalLayout = QtGui.QHBoxLayout(ListAssets)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.ListAssetsComboBox = QtGui.QComboBox(ListAssets)
        self.ListAssetsComboBox.setMaximumSize(QtCore.QSize(150, 30))
        self.ListAssetsComboBox.setObjectName("ListAssetsComboBox")
        self.verticalLayout.addWidget(self.ListAssetsComboBox)
        self.ListAssetsView = QtGui.QListView(ListAssets)
        self.ListAssetsView.setObjectName("ListAssetsView")
        self.verticalLayout.addWidget(self.ListAssetsView)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(ListAssets)
        QtCore.QObject.connect(self.ListAssetsView, QtCore.SIGNAL("clicked(QModelIndex)"), ListAssets.emitAssetId)
        QtCore.QObject.connect(self.ListAssetsComboBox, QtCore.SIGNAL("currentIndexChanged(int)"), ListAssets.setFilter)
        QtCore.QObject.connect(self.ListAssetsComboBox, QtCore.SIGNAL("currentIndexChanged(int)"), ListAssets.emitAssetType)
        QtCore.QMetaObject.connectSlotsByName(ListAssets)

    def retranslateUi(self, ListAssets):
        ListAssets.setWindowTitle(QtGui.QApplication.translate("ListAssets", "Form", None, QtGui.QApplication.UnicodeUTF8))

