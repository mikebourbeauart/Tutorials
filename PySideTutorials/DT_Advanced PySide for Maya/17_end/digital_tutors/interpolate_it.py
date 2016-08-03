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
        self.slider_down = False

        store_items.clicked.connect(self.storeItems)
        clear_items.clicked.connect(self.clearItems)

        self.store_start_bttn.clicked.connect(self.storeStart)
        self.store_end_bttn.clicked.connect(self.storeEnd)

    #------------------------------------------------------------------------------------------#

    def _startSliderUndo(self):
        pm.undoInfo(openChunk=True)


    def _endSliderUndo(self):
        pm.undoInfo(closeChunk=True)
        self.slider_down = False

    #------------------------------------------------------------------------------------------#

    def storeItems(self):
        selection = pm.ls(sl=True, fl=True)
        if not selection:
            return False

        self.items = {}
        for node in selection:
            self.items[node.name()] = {NODE:node, START:{}, END:{}, CACHE:{}}

        self.enableButtons(True)


    def clearItems(self):
        self.items = {}
        self.enableButtons(False)

    #------------------------------------------------------------------------------------------#

    def enableButtons(self, value):
        self.store_start_bttn.setEnabled(value)
        self.reset_item_bttn.setEnabled(value)
        self.store_end_bttn.setEnabled(value)
        self.transforms_chbx.setEnabled(value)
        self.attributes_chbx.setEnabled(value)
        self.slider.setEnabled(value)
        self.start_lb.setEnabled(value)
        self.end_lb.setEnabled(value)

    #------------------------------------------------------------------------------------------#

    def storeStart(self):
        if not self.items: return
        self._store(START, 0)


    def storeEnd(self):
        if not self.items: return
        self._store(END, 50)


    def _store(self, key, value):
        for item_dict in self.items.values():
            node  = item_dict[NODE]
            attrs = self.getAttributes(node)
            data  = item_dict[key]
            for attr in attrs:
                data[attr] = node.attr(attr).get()

            print item_dict

        self.slider.blockSignals(True)
        self.slider.setValue(value)
        self.slider.blockSignals(False)

    #------------------------------------------------------------------------------------------#

    def getAttributes(self, node):
        attrs = []
        if self.transforms_chbx.isChecked():
            for transform in 'trs':
                for axis in 'xyz':
                    channel = '%s%s' %(transform, axis)
                    if node.attr(channel).isLocked(): continue
                    attrs.append(channel)

        return attrs

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
