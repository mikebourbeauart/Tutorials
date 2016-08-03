from PySide import QtGui, QtCore 
from shiboken import wrapInstance 
import maya.cmds as mc
import maya.OpenMayaUI as mui


class ToolTipFilter(QtCore.QObject):
    '''A simple event filter to catch tooltip events'''
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.ToolTip:
            QtGui.QToolTip.hideText() 
            QtGui.QToolTip.showText(event.globalPos(), '%04f, %04f'%(event.globalX(), event.globalY()), obj)
            return False
        return True


global filter 
filter = ToolTipFilter()

for editor in mc.lsUI(panels=True): 
    if mc.objectTypeUI(editor)=='modelEditor':
        ptr = mui.MQtUtil.mainWindow()
        viewWidget = wrapInstance( long( ptr ), QtGui.QWidget ) 
        viewWidget.installEventFilter(filter)



