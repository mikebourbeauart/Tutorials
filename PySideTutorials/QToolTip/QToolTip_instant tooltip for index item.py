from PySide import QtCore, QtGui
import sys
from shiboken import wrapInstance
import maya.OpenMayaUI as mui

def get_parent():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance( long( ptr ), QtGui.QWidget )  
     
class Window(QtGui.QDialog):
    def __init__(self, parent=get_parent() ):
        super(Window, self).__init__( parent )
        
        self.view = QtGui.QTreeView(self)
        self.view.setMouseTracking(True)
        
        self.view.entered.connect(self.handleItemEntered)
        
        model = QtGui.QStandardItemModel(self)
        
        for text in 'One Two Three Four Five'.split():
            model.appendRow(QtGui.QStandardItem(text))
            
        self.view.setModel(model)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.view)

    def handleItemEntered(self, index):
        if index.isValid():
            QtGui.QToolTip.showText(
                QtGui.QCursor.pos(),
                index.data(),
                self.view.viewport(),
                self.view.visualRect(index)
                )
    
if __name__ == "__main__":
    # workaround for a bug in maya
    try:
        my_window.close()
        my_window.deleteLater()
    except:
        pass
        
    my_window = Window()
    my_window.setGeometry(500, 300, 200, 200)
    my_window.show()

    try:
        my_window.show()
    except:
        my_window.close()
        my_window.deleteLater()