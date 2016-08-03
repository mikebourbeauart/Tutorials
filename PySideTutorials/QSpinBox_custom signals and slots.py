from PySide import QtCore, QtGui
from shiboken import wrapInstance 
import maya.OpenMayaUI as mui

def maya_main_window():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance( long( ptr ), QtGui.QWidget )   

class ZeroSpinBox(QtGui.QSpinBox):
    atzero = QtCore.Signal(int)

    zeros = 0

    def __init__(self):
        super(ZeroSpinBox, self).__init__()
        
        self.valueChanged.connect(self.checkzero)

    def checkzero(self):
        if self.value() == 0:
            self.zeros += 1
            #self.emit(SIGNAL("atzero(int)"), self.zeros)
            self.atzero.emit(self.zeros)



class Form(QtGui.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(Form, self).__init__(parent)

        dial = QtGui.QDial()
        dial.setNotchesVisible(True)
        zerospinbox = ZeroSpinBox()
        layout = QtGui.QHBoxLayout()
        layout.addWidget(dial)
        layout.addWidget(zerospinbox)
        self.setLayout(layout)

        dial.valueChanged.connect(zerospinbox.setValue)
        zerospinbox.valueChanged.connect(dial.setValue)
        zerospinbox.atzero.connect(self.announce)
#         self.connect(zerospinbox, SIGNAL("atzero(int)"), self.announce)

        self.setWindowTitle("Signals")

    def announce(self, zeros):
        print("zerospinbox has been at zero " + str(zeros) + " times.")


if __name__ == "__main__": 
    # Development stuff
    try:
        form.close()
        form.deleteLater()
    except:
        pass


    form = Form()
    form.show()


    # Development stuff
    try:
        form.show()
    except:
        form.close()
        form.deleteLater()


