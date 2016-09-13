# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ListAssetVersions.ui'
#
# Created: Fri Apr 12 12:02:31 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ListAssetVersions(object):
    def setupUi(self, ListAssetVersions):
        ListAssetVersions.setObjectName("ListAssetVersions")
        ListAssetVersions.resize(175, 297)
        ListAssetVersions.setMinimumSize(QtCore.QSize(175, 0))
        ListAssetVersions.setMaximumSize(QtCore.QSize(175, 16777215))
        self.horizontalLayout = QtGui.QHBoxLayout(ListAssetVersions)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ListAssetVersionsView = QtGui.QListView(ListAssetVersions)
        self.ListAssetVersionsView.setObjectName("ListAssetVersionsView")
        self.horizontalLayout.addWidget(self.ListAssetVersionsView)

        self.retranslateUi(ListAssetVersions)
        QtCore.QObject.connect(self.ListAssetVersionsView, QtCore.SIGNAL("clicked(QModelIndex)"), ListAssetVersions.emitAssetVersionId)
        QtCore.QMetaObject.connectSlotsByName(ListAssetVersions)

    def retranslateUi(self, ListAssetVersions):
        ListAssetVersions.setWindowTitle(QtGui.QApplication.translate("ListAssetVersions", "Form", None, QtGui.QApplication.UnicodeUTF8))

