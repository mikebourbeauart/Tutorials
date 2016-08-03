from PySide import QtCore, QtGui
from shiboken import wrapInstance 
import maya.OpenMayaUI as mui

def maya_main_window():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance( long( ptr ), QtGui.QWidget )   

####################################################################
class MyWindow(QtGui.QDialog): 
    def __init__( self, parent=maya_main_window() ):
        super( MyWindow, self ).__init__(  )
        
        self.word_list = ['alpha', 'beta', 'car', 'hello', 'bye']
        # create objects
        self.la = QtGui.QLabel("Press tab in this box:")
        self.le = MyLineEdit()
        self.completer = QtGui.QCompleter(self.word_list)
        self.le.setCompleter(self.completer)
        self.la2 = QtGui.QLabel("\nLook here:")
        self.le2 = QtGui.QLineEdit()

        # layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.la)
        layout.addWidget(self.le)
        layout.addWidget(self.la2)
        layout.addWidget(self.le2)
        self.setLayout(layout)

        # connections
        #self.connect(self.le, QtCore.SIGNAL("tabPressed"), self.update)
        self.le.tab_pressed.connect(self.update)
        
    # Slot
    def update(self):
        newtext = str(self.le2.text()) + "tab pressed "
        self.le2.setText(newtext)

####################################################################
class MyLineEdit( QtGui.QLineEdit):
    
    # Signal specific variables
    tab_pressed = QtCore.Signal(str)
    signal_str = "tabPressed"
    
    def __init__(self, parent=None):
        super( MyLineEdit, self ).__init__(   )
    
    #Signal
    def event(self, event):
        
        if (event.type()==QtCore.QEvent.KeyPress) and (event.key()==QtCore.Qt.Key_Tab):
            self.tab_pressed.emit(self.signal_str)
            return True

        return QtGui.QLineEdit.event(self, event)

####################################################################
if __name__ == "__main__": 
# Development stuff
    try:
        myWindow_ui.close()
        myWindow_ui.deleteLater()
    except:
        pass

    myWindow_ui = MyWindow()
    myWindow_ui.show()

    # Development stuff
    try:
        myWindow_ui.show()
    except:
        myWindow_ui.close()
        myWindow_ui.deleteLater()