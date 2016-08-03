import PyQt4.QtCore as qc
import PyQt4.QtGui  as qg

import maya.cmds  as mc
import pymel.core as pm
from utils.generic import undo

import maya.OpenMayaUI as mui
import sip

START      = 'start'
END        = 'end'
CACHE      = 'cache'
NODE       = 'node'


class InterpolateIt(qg.QDialog):
    def __init__(self):
        qg.QDialog.__init__(self)
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setObjectName('InterpolateIt')
        self.setWindowTitle('Interpolate It')
        self.setFixedWidth(314)

        self.setLayout(qg.QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)

        scroll_area = qg.QScrollArea()
        scroll_area.setFocusPolicy(qc.Qt.NoFocus)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(qc.Qt.ScrollBarAlwaysOff)
        self.layout().addWidget(scroll_area)

        main_widget = qg.QWidget()
        main_layout = qg.QVBoxLayout()
        main_layout.setContentsMargins(5,5,5,5)
        main_layout.setAlignment(qc.Qt.AlignTop)
        main_widget.setLayout(main_layout)
        scroll_area.setWidget(main_widget)

        self.interp_layout = qg.QVBoxLayout()
        self.interp_layout.setContentsMargins(0,0,0,0)
        self.interp_layout.setSpacing(0)
        self.interp_layout.setAlignment(qc.Qt.AlignTop)
        main_layout.addLayout(self.interp_layout)

        button_layout = qg.QHBoxLayout()
        button_layout.setContentsMargins(0,0,0,0)
        button_layout.setAlignment(qc.Qt.AlignRight)
        main_layout.addLayout(button_layout)

        add_button = qg.QPushButton('New...', parent=self)
        button_layout.addWidget(add_button)

        new_widget = InterpolateWidget()
        self.interp_layout.addWidget(new_widget)

        self._interp_widget = []
        self._interp_widget.append(new_widget)

        self._dock_widget = self._dock_name = None

        add_button.clicked.connect(self.add)

    #------------------------------------------------------------------------------------------#

    def add(self):
        new_widget = InterpolateWidget()
        self.interp_layout.addWidget(new_widget)
        self._interp_widget.append(new_widget)


    def remove(self, interp_widget):
        self._interp_widget.remove(interp_widget)

    #------------------------------------------------------------------------------------------#

    def connectDockWidget(self, dock_name, dock_widget):
        self._dock_widget = dock_widget
        self._dock_name   = dock_name


    def close(self):
        if self._dock_widget:
            mc.deleteUI(self._dock_name)
        else:
            qg.QDialog.close(self)
        self._dock_widget = self._dock_name = None

#--------------------------------------------------------------------------------------------------#

class InterpolateWidget(qg.QFrame):
    def __init__(self, *args, **kwargs):
        qg.QFrame.__init__(self, *args, **kwargs)

        self.setLayout(qg.QVBoxLayout())
        self.layout().setContentsMargins(5,5,5,5)
        self.layout().setSpacing(0)
        self.setFrameStyle(qg.QFrame.Panel | qg.QFrame.Raised)
        self.setFixedHeight(150)

        self.main_widget = qg.QWidget()
        self.main_widget.setObjectName('mainWidget')
        self.main_widget.setLayout(qg.QVBoxLayout())
        self.main_widget.layout().setContentsMargins(2,2,2,2)
        self.main_widget.layout().setSpacing(5)
        self.layout().addWidget(self.main_widget)

        select_layout = qg.QHBoxLayout()
        button_layout = qg.QHBoxLayout()
        slider_layout = qg.QHBoxLayout()
        check_layout  = qg.QHBoxLayout()
        self.main_widget.layout().addLayout(select_layout)
        self.main_widget.layout().addLayout(button_layout)
        self.main_widget.layout().addLayout(slider_layout)
        self.main_widget.layout().addLayout(check_layout)

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
        self.reset_item_bttn.clicked.connect(self.resetAttributes)
        self.store_end_bttn.clicked.connect(self.storeEnd)

        self.slider.valueChanged.connect(self.setLinearInterpolation)

        self.slider.sliderReleased.connect(self._endSliderUndo)

        self.enableButtons(False)

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
        self._cache()


    def storeEnd(self):
        if not self.items: return
        self._store(END, 50)
        self._cache()


    def _store(self, key, value):
        for item_dict in self.items.values():
            node  = item_dict[NODE]
            attrs = self.getAttributes(node)
            data  = item_dict[key]
            for attr in attrs:
                data[attr] = node.attr(attr).get()

        self.slider.blockSignals(True)
        self.slider.setValue(value)
        self.slider.blockSignals(False)


    def _cache(self):
        for item_dict in self.items.values():
            node  = item_dict[NODE]

            start = item_dict[START]
            end   = item_dict[END]
            if not start or not end:
                item_dict[CACHE] = None
                continue

            attrs = list(set(start.keys()) and set(end.keys()))

            cache = item_dict[CACHE] = {}
            for attr in attrs:
                start_attr = start[attr]
                end_attr   = end[attr]
                if start_attr == end_attr:
                    cache[attr] = None
                else:
                    cache_values = cache[attr] = []
                    interval    = float(end_attr - start_attr) / 49.0
                    for index in range(50):
                        cache_values.append((interval * index) + start_attr)

    #------------------------------------------------------------------------------------------#

    def getAttributes(self, node):
        attrs = []
        if self.transforms_chbx.isChecked():
            for transform in 'trs':
                for axis in 'xyz':
                    channel = '%s%s' %(transform, axis)
                    if node.attr(channel).isLocked(): continue
                    attrs.append(channel)

        if self.attributes_chbx.isChecked():
            for attr in node.listAttr(ud=True):
                if attr.isLocked(): continue
                if attr.type() not in ('double', 'int'): continue

                attrs.append(attr.name().split('.')[-1])

        return attrs


    def resetAttributes(self):
        if not self.items:
            return

        for item_dict in self.items.values():
            node  = item_dict[NODE]
            attrs = self.getAttributes(node)

            for attr in attrs:
                default_value = pm.attributeQuery(attr, node=node, ld=True)[0]
                node.attr(attr).set(default_value)

    #------------------------------------------------------------------------------------------#

    def setLinearInterpolation(self, value):
        if not self.items:
            return

        if not self.slider_down:
            self._startSliderUndo()
            self.slider_down = True

        for item_dict in self.items.values():
            node  = item_dict[NODE]
            start = item_dict[START]

            if not start or not item_dict[END]: continue

            cache = item_dict[CACHE]

            for attr in cache.keys():
                if cache[attr] == None: continue
                node.attr(attr).set(cache[attr][value])

#--------------------------------------------------------------------------------------------------#

dialog = None

def create(docked=True):
    global dialog

    if dialog is None:
        dialog = InterpolateIt()

    if docked is True:
        ptr = mui.MQtUtil.mainWindow()
        main_window = sip.wrapinstance(long(ptr), qc.QObject)

        dialog.setParent(main_window)
        size = dialog.size()

        name = mui.MQtUtil.fullName(long(sip.unwrapinstance(dialog)))
        dock = mc.dockControl(
            allowedArea =['right', 'left'],
            area        = 'right',
            floating    = False,
            content     = name,
            width       = size.width(),
            height      = size.height(),
            label       = 'Interpolate It')

        widget      = mui.MQtUtil.findControl(dock)
        dock_widget = sip.wrapinstance(long(widget), qc.QObject)
        dialog.connectDockWidget(dock, dock_widget)

    else:
        dialog.show()


def delete():
    global dialog
    if dialog:
        dialog.close()
        dialog = None
