from PySide import QtCore, QtGui 
from shiboken import wrapInstance 
import maya.OpenMayaUI as mui 

mainWin = wrapInstance(long(mui.MQtUtil.mainWindow()), QtGui.QWidget) 

action = QtGui.QAction(mainWin) 
action.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Tab)) 
action.setShortcutContext(QtCore.Qt.ApplicationShortcut) 

def foo(): 
    print "TAB!" 
    
action.triggered.connect(foo) 
mainWin.addAction(action) 