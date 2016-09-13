import PyQt4.QtCore as qc
import PyQt4.QtGui  as qg

import utils.names as names
import maya.cmds   as mc

dialog = None

#------------------------------------------------------------------------------#

class NameIt(qg.QDialog):
    def __init__(self):
        qg.QDialog.__init__(self)
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Name It')
        self.setFixedHeight(285)
        self.setFixedWidth(320)

        self.setLayout(qg.QVBoxLayout())
        self.layout().setContentsMargins(5,5,5,5)
        self.layout().setSpacing(0)
        self.layout().setAlignment(qc.Qt.AlignTop)

        # RENAME Widget
        #
        rename_widget = qg.QWidget()
        rename_widget.setLayout(qg.QVBoxLayout())
        rename_widget.layout().setContentsMargins(0,0,0,0)
        rename_widget.layout().setSpacing(2)
        rename_widget.setSizePolicy(qg.QSizePolicy.Minimum,
                                    qg.QSizePolicy.Fixed)
        self.layout().addWidget(rename_widget)

        # REPLACE Widget
        #
        replace_widget = qg.QWidget()
        replace_widget.setLayout(qg.QVBoxLayout())
        replace_widget.layout().setContentsMargins(0,0,0,0)
        replace_widget.layout().setSpacing(2)
        replace_widget.setSizePolicy(qg.QSizePolicy.Minimum,
                                     qg.QSizePolicy.Fixed)
        self.layout().addWidget(replace_widget)

#------------------------------------------------------------------------------#

def create():
    global dialog
    if dialog is None:
        dialog = NameIt()
    dialog.show()


def delete():
    global dialog
    if dialog is None:
        return

    dialog.deleteLater()
    dialog = None
