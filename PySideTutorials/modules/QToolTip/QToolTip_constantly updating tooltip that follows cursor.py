from PySide import QtGui, QtCore
import maya.OpenMayaUI as mui

def get_parent():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance( long( ptr ), QtGui.QWidget )   

class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
    def initUI(self):      
        hbox = QtGui.QHBoxLayout(self)
        self.lbl = MyLabel(self)
        self.lbl.setText("foo")
        self.lbl.setToolTip("bar")
        hbox.addWidget(self.lbl)
        label2 = QtGui.QLabel('another label')
        hbox.addWidget(label2)
        label2.setToolTip('a normal tooltip')
        self.setLayout(hbox)
        self.show()
        
class MyLabel(QtGui.QLabel):
    def __init__(self,*args,**kwargs):
        QtGui.QLabel.__init__(self,*args,**kwargs)
        self._timer = QtCore.QBasicTimer()
        self._timer.start(100, self)
        self._value = 0
        self._last_event_pos = None

    def event(self,event):
        if event.type() == QtCore.QEvent.ToolTip:
            self._last_event_pos = event.globalPos()
            return True
        elif event.type() == QtCore.QEvent.Leave:
            self._last_event_pos = None
            QtGui.QToolTip.hideText()
        return QtGui.QLabel.event(self,event)

    def timerEvent(self, x):
        self._value += 1
        if self._last_event_pos:
            QtGui.QToolTip.hideText()
            QtGui.QToolTip.showText(self._last_event_pos, "bar: %03d" % self._value)
        self.setText("foo: %03d" % self._value)
        
'''
# Another way to do the label
class MyLabel(QtGui.QLabel):
    def __init__(self,*args,**kwargs):
        QtGui.QLabel.__init__(self,*args,**kwargs)
        self._setToolTip=QtGui.QLabel.setToolTip
        self._last_event_pos = None
        self._tooltip=QtGui.QLabel.toolTip(self)
        
    def event(self,event):
        if event.type() == QtCore.QEvent.ToolTip:
            self._last_event_pos = event.globalPos()
            return True
        elif event.type() == QtCore.QEvent.Leave:
            self._last_event_pos = None
            QtGui.QToolTip.hideText()
        return QtGui.QLabel.event(self,event)
        
    def setToolTip(self, tt):
        self._setToolTip(self, tt)
        if self._last_event_pos:
            QtGui.QToolTip.hideText()
            QtGui.QToolTip.showText(self._last_event_pos,
                                    QtGui.QLabel.toolTip(self))
'''
############################################
if __name__ == "__main__":
    try:
        ex_ui.close()
        ex_ui.deleteLater()
    except:
        pass
        
    ex_ui = Example()
    ex_ui.show()

    try:
        ex_ui.show()
    except:
        ex_ui.close()
        ex_ui.deleteLater()