import PyQt4.QtCore as qc
import PyQt4.QtGui  as qg

import maya.cmds  as mc
import pymel.core as pm
from utils.generic import undo_pm
from functools import partial


START      = 'start'
END        = 'end'
CACHE      = 'cache'
NODE       = 'node'


class InterpolateIt(qg.QDialog):
    def __init__(self):
        qg.QDialog.__init__(self)
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Interpolate It')

        self.setLayout(qg.QVBoxLayout())
        self.layout().setContentsMargins(5,5,5,5)
        self.layout().setSpacing(5)

        select_layout = qg.QHBoxLayout()
        button_layout = qg.QHBoxLayout()
        slider_layout = qg.QHBoxLayout()
        check_layout  = qg.QHBoxLayout()
        self.layout().addLayout(select_layout)
        self.layout().addLayout(button_layout)
        self.layout().addLayout(slider_layout)
        self.layout().addLayout(check_layout)

        store_items = qg.QPushButton('Store Items')
        clear_items = qg.QPushButton('Clear Items')

        select_layout.addSpacerItem(qg.QSpacerItem(5, 5, qg.QSizePolicy.Expanding))
        select_layout.addWidget(store_items)
        select_layout.addWidget(clear_items)
        select_layout.addSpacerItem(qg.QSpacerItem(5, 5, qg.QSizePolicy.Expanding))

        self.store_start_bttn = qg.QPushButton('Store Start')
        self.reset_item_bttn  = qg.QPushButton('Reset')
        self.store_end_bttn   = qg.QPushButton('Store End')

        button_layout.addWidget(self.store_start_bttn)
        button_layout.addWidget(self.reset_item_bttn)
        button_layout.addWidget(self.store_end_bttn)

        self.start_lb = qg.QLabel('Start')
        self.slider = qg.QSlider()
        self.slider.setRange(0, 49)
        self.slider.setOrientation(qc.Qt.Horizontal)
        self.end_lb = qg.QLabel('End')

        slider_layout.addWidget(self.start_lb)
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.end_lb)

        self.transforms_chbx = qg.QCheckBox('Transform')
        self.attributes_chbx = qg.QCheckBox('UD Attributes')
        self.transforms_chbx.setCheckState(qc.Qt.Checked)
        check_layout.addWidget(self.transforms_chbx)
        check_layout.addWidget(self.attributes_chbx)

        self.items = {}

    #------------------------------------------------------------------------------------------#

    def storeItems(self):
        selection = pm.ls(sl=True, fl=True)
        if not selection:
            return False

        self.items = {}
        for node in selection:
            self.items[node.name()] = {NODE:node, START:{}, END:{}, CACHE:{}}

        self.enableButtons(True)

#--------------------------------------------------------------------------------------------------#

dialog = None

def create():
    global dialog
    if dialog is None:
        dialog = InterpolateIt()
    dialog.show()


def delete():
    global dialog
    if dialog is None:
        return

    dialog.deleteLater()
    dialog = None
