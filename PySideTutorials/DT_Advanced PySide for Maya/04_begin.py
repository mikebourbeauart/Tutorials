import PyQt4.QtCore as qc
import PyQt4.QtGui as qg

class simpleUI(qg.QDialog):
    def __init__(self):
        qg.QDialog.__init__(self)
        self.setWindowTitle('Simple UI')
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setModal(False)
        self.setFixedHeight(250)
        self.setFixedWidth(300)

dialog = simpleUI()
dialog.show()
