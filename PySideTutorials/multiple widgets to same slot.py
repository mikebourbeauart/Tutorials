# Example formatted by Mike Bourbeau for Maya PySide from here: http://www.blog.pythonlibrary.org/2013/04/10/pyside-connecting-multiple-widgets-to-the-same-slot/

from PySide import QtCore, QtGui
from shiboken import wrapInstance
import maya.OpenMayaUI as mui

def maya_main_window():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance( long( ptr ), QtGui.QWidget )   
        
 
########################################################################
class MultiButtonDemo(QtGui.QDialog):
    """Constructor"""
    def __init__(self, parent=maya_main_window()):
        super(MultiButtonDemo, self).__init__(parent)
        
        # Create the main layout
        self.main_layout = QtGui.QVBoxLayout()
        # Create the buttons
        label_names = ["One", "Two", "Three", "Four"]
        for name in label_names:
            self.btn = QtGui.QPushButton(name)
            self.btn.clicked.connect(self.was_clicked)
            self.main_layout.addWidget(self.btn)
        
        # Create the UI 
        self.ui_label = QtGui.QLabel("You haven't pressed a button!")
        self.main_layout.addWidget(self.ui_label)
        self.setLayout(self.main_layout)
        self.setWindowTitle("PySide Signals / Slots Demo")
        
    #----------------------------------------------------------------------
    # Slots
    #----------------------------------------------------------------------
    def was_clicked(self):
        """
        Change label based on what button was pressed
        """
        ui_button = self.sender()
        if isinstance(ui_button, QtGui.QPushButton):
            self.ui_label.setText("You pressed {0}!".format(ui_button.text()))

 
#----------------------------------------------------------------------
if __name__ == "__main__":
    # Development stuff
    try:
        multiButtonDemo_ui.close()
        multiButtonDemo_ui.deleteLater()
    except:
        pass
    
    multiButtonDemo_ui = MultiButtonDemo()
    multiButtonDemo_ui.show()

    # Development stuff
    try:
        multiButtonDemo_ui.show()
    except:
        multiButtonDemo_ui.close()
        multiButtonDemo_ui.deleteLater()

