from PySide import QtCore, QtGui
from shiboken import wrapInstance
import maya.OpenMayaUI as mui

def getMayaWindow():
    '''
    Get the maya main window as a QMainWindow instance
    '''
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance( long( ptr ), QtGui.QWidget )

class TabMenu(QtGui.QAction):
    
    def __init__(self, parent=getMayaWindow()):
        super(TabMenu, self).__init__(parent)
    
    mainWin = wrapInstance(long(mui.MQtUtil.mainWindow()), QtGui.QWidget)

    action = QtGui.QAction(mainWin)
    action.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Tab))
    action.setShortcutContext(QtCore.Qt.ApplicationShortcut)

    def foo():
        print "jhfdjh!"

    action.triggered.connect(foo)
    mainWin.addAction(action)