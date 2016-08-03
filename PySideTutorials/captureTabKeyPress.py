from PySide import QtCore, QtGui
from shiboken import wrapInstance 
import maya.OpenMayaUI as mui

def maya_main_window():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance( long( ptr ), QtGui.QWidget )   

####################################################################
class MyWindow(QtGui.QDialog): 
    def __init__( self, parent=maya_main_window()):
        super( MyWindow, self ).__init__( parent )
               
        self.move_UI()
        self.create_gui()
        self.create_layout()
        self.create_connections()
        self.setAttribute( QtCore.Qt.WA_DeleteOnClose ) 
        
    def move_UI(self):
        ''' Moves the UI to the cursor's position '''
        pos = QtGui.QCursor.pos()
        self.move(pos.x()-100, pos.y()-150)
        
            
    def create_gui(self):
        word_list = ['alpha', 'beta', 'car', 'hello', 'bye']
        self.la = QtGui.QLabel("Press tab in this box:")
        self.le = MyLineEdit()
        self.completer = QtGui.QCompleter(word_list)
        self.le.setCompleter(self.completer)
        self.la2 = QtGui.QLabel("\nLook here:")
        self.le2 = QtGui.QLineEdit()

    def create_layout(self):
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.la)
        layout.addWidget(self.le)
        layout.addWidget(self.la2)
        layout.addWidget(self.le2)
        layout.totalMaximumSize()
        layout.addStretch()
        self.setLayout(layout)

    def create_connections(self):
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
    
        self.setFixedHeight(25)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        self.setFont(font)
    
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