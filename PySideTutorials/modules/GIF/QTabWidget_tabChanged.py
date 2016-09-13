import sys, os
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
from PySide.QtNetwork import *
from PySide import QtCore, QtGui, QtWebKit
from PySide.QtWebKit import QWebView


class BaseWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.centralWidget = QtGui.QWidget()
        self.resize(800, 500)
        self.setWindowTitle('Test')
        self.tabs = QTabWidget()

        self.tabs.blockSignals(True) #just for not showing the initial message
        self.tabs.currentChanged.connect(self.onChange) #changed!


        self.webview = QWebView()
        self.webview.load(QUrl("http://gmx.de"))

        self.webview2 = QWebView()
        self.webview2.load(QUrl("http://web.de"))

        centralLayout = QtGui.QVBoxLayout()
        centralLayout.addWidget(self.tabs, 1)

        self.tabs.addTab(self.webview, "gmx")
        self.tabs.addTab(self.webview2, "web")
        self.centralWidget.setLayout(centralLayout)

        self.setCentralWidget(self.centralWidget)

        self.tabs.blockSignals(False) #now listen the currentChanged signal


    #@pyqtSlot()
    def onChange(self,i): #changed!
        QtGui.QMessageBox.information(self,
                  "Tab Index Changed!",
                  "Current Tab Index: %d" % i ) #changed!

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = BaseWindow()
    window.show()
    sys.exit(app.exec_())