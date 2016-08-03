from PySide import QtCore
from PySide import QtGui
from shiboken import wrapInstance

class SimpleUI( QtGui.QDialog ):
    def __init__(self):
        super(SimpleUI, self).__init__()
        
        self.setWindowTitle('Simple UI')
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        
        self.setLayout(QtGui.QVBoxLayout())
        
        
dialog = SimpleUI()
dialog.show()