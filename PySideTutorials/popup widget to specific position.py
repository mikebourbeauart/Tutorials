from PySide import QtCore, QtGui
from shiboken import wrapInstance 

def get_parent():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance( long( ptr ), QtGui.QWidget )


class My_Window(QtGui.QDialog):
    def __init__(self, parent=get_parent()):
        super(My_Window, self).__init__(parent)
        self.button = QtGui.QPushButton('Hit this button to show a popup', self)
        self.button.clicked.connect(self.handleOpenDialog)
        self.button.move(250, 50)
        self.resize(600, 200)

    def handleOpenDialog(self):
        self.popup_ui = popup(self.button)
        self.popup_ui.show()

class popup(QtGui.QWidget):
    def __init__(self, widget=None):    
        super(popup, self).__init__()
        
        layout = QtGui.QGridLayout(self)
        button = QtGui.QPushButton("Very Interesting Text Popup. Here's an arrow   ^")
        layout.addWidget(button)
        
        # adjust the margins or you will get an invisible, unintended border
        layout.setContentsMargins(0, 0, 0, 0)
        
        # need to set the layout
        self.setLayout(layout)
        self.adjustSize()
        
         # tag this widget as a popup
        self.setWindowFlags(QtCore.Qt.Popup)
        
        # Get y button position                                          
        global_point = widget.mapToGlobal(widget.rect().topLeft() )


        # by default, a widget will be placed from its top-left corner, so
        # we need to move it to the left based on the widgets width
        self.move(global_point - QtCore.QPoint(self.width(), 0)) 


if __name__ == '__main__':
    # Things to fix PySide Maya bug
    try:
        test_ui.close()
        test_ui.deleteLater()
    except:
        pass
        
    test_ui = My_Window()
    test_ui.show()

    try:
        test_ui.show()
    except:
        test_ui.close()
        test_ui.deleteLater()