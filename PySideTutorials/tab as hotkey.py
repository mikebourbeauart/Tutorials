from PySide import QtCore, QtGui
from shiboken import wrapInstance 
import maya.OpenMayaUI as mui

mainWin = wrapInstance(long(mui.MQtUtil.mainWindow()), QtGui.QWidget)

action = QtGui.QAction(mainWin)
action.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Y))
action.setShortcutContext(QtCore.Qt.ApplicationShortcut)

def foo():
    import mb_pandora_master
    reload(mb_pandora_master)
    mb_pandora_master.run()
    print "tabbed"
    
action.triggered.connect(foo)
mainWin.addAction(action)