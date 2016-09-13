from PySide import QtCore, QtGui
from shiboken import wrapInstance
import maya.OpenMayaUI as mui
import maya.OpenMaya as om
import maya.cmds as mc
import maya.mel as mel
import os

def get_parent():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance( long( ptr ), QtGui.QWidget )   

############################################        
''' Classes '''
############################################
class QCustomQWidget (QtGui.QWidget):
    def __init__ (self, parent = get_parent() ):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QtGui.QVBoxLayout()
        self.textUpQLabel    = QtGui.QLabel()
        self.textDownQLabel  = QtGui.QLabel()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout  = QtGui.QHBoxLayout()
        self.iconQLabel      = QtGui.QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.textUpQLabel.setStyleSheet('''
            color: rgb(0, 0, 255);
        ''')
        self.textDownQLabel.setStyleSheet('''
            color: rgb(255, 0, 0);
        ''')

    def setTextUp (self, text):
        self.textUpQLabel.setText(text)

    def setTextDown (self, text):
        self.textDownQLabel.setText(text)

    def setIcon (self, imagePath):
        self.iconQLabel.setPixmap(QtGui.QPixmap(imagePath))

class exampleQMainWindow (QtGui.QMainWindow):
    def __init__ (self):
        super(exampleQMainWindow, self).__init__()
        
        # Create QListWidget
        self.myQListWidget = QtGui.QListWidget(self)
        for file, name, other, icon in [
            ('No.1', 'Meyoko', 'hey\nyou',  ":/menuIconFile.png"),
            ('No.2', 'Nyaruko', 'hey', ":/menuIconFile.png"),
            ('No.3', 'Louise', 'hey',  ":/menuIconFile.png")]:
            # Create QCustomQWidget
            myQCustomQWidget = QCustomQWidget()
            #myQCustomQWidget.setTextUp(index)
            myQCustomQWidget.setTextUp(other)
            myQCustomQWidget.setTextDown(name)
            myQCustomQWidget.setIcon(icon)
            # Create QListWidgetItem
            myQListWidgetItem = QtGui.QListWidgetItem(self.myQListWidget)
            # Set size hint
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            # Add QListWidgetItem into QListWidget
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        self.setCentralWidget(self.myQListWidget)

# Development stuff
try:
    window.close()
    window.deleteLater()
except:
    pass

# Show stuff
window = exampleQMainWindow()
window.show()

# Development stuff
try:
    window.show()
except:
    window.close()
    window.deleteLater()