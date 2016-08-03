import PyQt4.QtCore as qc
import PyQt4.QtGui as qg

from functools import partial

class simpleUI(qg.QDialog):
    def __init__(self):
        qg.QDialog.__init__(self)
        self.setWindowTitle('Simple UI')
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setModal(False)
        self.setFixedHeight(250)
        self.setMinimumWidth(300)

        self.setLayout(qg.QVBoxLayout())
        self.layout().setContentsMargins(5,5,5,5)
        self.layout().setSpacing(0)
        self.layout().setAlignment(qc.Qt.AlignTop)

        top_frame    = qg.QFrame()
        top_frame.setFrameStyle(qg.QFrame.Panel | qg.QFrame.Raised)
        middle_frame = qg.QFrame()
        middle_frame.setFrameStyle(qg.QFrame.Panel | qg.QFrame.Raised)
        bttm_frame   = qg.QFrame()
        bttm_frame.setFrameStyle(qg.QFrame.Panel | qg.QFrame.Raised)

        #self.layout().addWidget(top_frame)
        self.layout().addWidget(middle_frame)
        #self.layout().addWidget(bttm_frame)

        middle_frame.setLayout(qg.QHBoxLayout())
        middle_frame.layout().setContentsMargins(5,5,5,5)
        middle_frame.layout().setSpacing(0)
        middle_frame.layout().setAlignment(qc.Qt.AlignTop)

        middle_frame.setSizePolicy(qg.QSizePolicy.Minimum, qg.QSizePolicy.Fixed)

        bttn_1 = qg.QPushButton('1')
        bttn_2 = qg.QPushButton('2')
        bttn_3 = qg.QPushButton('3')
        bttn_4 = qg.QPushButton('4')
        bttn_5 = qg.QPushButton('5')

        middle_frame.layout().addWidget(bttn_1)
        middle_frame.layout().addWidget(bttn_2)
        middle_frame.layout().addWidget(bttn_3)
        middle_frame.layout().addWidget(bttn_4)
        middle_frame.layout().addWidget(bttn_5)

dialog = simpleUI()
dialog.show()
