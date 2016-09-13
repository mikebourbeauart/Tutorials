import PyQt4.QtCore as qc
import PyQt4.QtGui  as qg

import maya.cmds  as mc
import pymel.core as pm
from utils.generic import undo_pm

import maya.OpenMaya as om
import maya.OpenMayaUI as mui
import sip, os

from functools import partial

import widgets.label as label; reload(label)
from widgets.button import DT_Button, DT_ButtonThin, DT_CloseButton
from widgets.checkbox import DT_Checkbox
from widgets.label import DT_Label
from widgets.slider import DT_Slider
from widgets.line_edit import DT_LineEdit


START      = 'start'
END        = 'end'
CACHE      = 'cache'
NODE       = 'node'

class InterpolateIt(qg.QDialog):
    def __init__(self):
        qg.QDialog.__init__(self)
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Interpolate It')
        self.setObjectName('InterpolateIt')
        self.setFixedWidth(314)

        style_sheet_file = qc.QFile(os.path.join(os.path.dirname(__file__), 'stylesheets', 'scheme.qss'))
        style_sheet_file.open(qc.QFile.ReadOnly)
        self.setStyleSheet(qc.QLatin1String(style_sheet_file.readAll()))

        self.setLayout(qg.QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)

        scroll_area = qg.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFocusPolicy(qc.Qt.NoFocus)
        scroll_area.setHorizontalScrollBarPolicy(qc.Qt.ScrollBarAlwaysOff)
        self.layout().addWidget(scroll_area)

        main_widget = qg.QWidget()
        main_widget.setObjectName('InterpolateIt')
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

        add_button = DT_ButtonThin('New..')
        button_layout.addWidget(add_button)

        new_widget = InterpolateWidget()
        new_widget.hideCloseButton()
        self.interp_layout.addWidget(new_widget)

        self._interp_widgets = []
        self._interp_widgets.append(new_widget)

        self._dock_widget = self._dock_name = None

        add_button.clicked.connect(self.add)

        self._callback_id = om.MEventMessage.addEventCallback('SceneOpened', self.clearAll)
        del_callback = partial(om.MMessage.removeCallback, self._callback_id)
        self.destroyed.connect(del_callback)

    #------------------------------------------------------------------------------------------#

    def add(self):
        new_widget = InterpolateWidget()
        self.interp_layout.addWidget(new_widget)
        self._interp_widgets.append(new_widget)
        self.connect(new_widget, qc.SIGNAL('CLOSE'), self.remove)
        new_widget.setFixedHeight(0)
        new_widget._animateExpand(True)


    def remove(self, interp_widget):
        self.connect(interp_widget, qc.SIGNAL('DELETE'), self._delete)
        self._interp_widgets.remove(interp_widget)
        interp_widget._animateExpand(False)


    def _delete(self, interp_widget):
        self.interp_layout.removeWidget(interp_widget)
        interp_widget._animation = None
        interp_widget.deleteLater()

    #-----------------------------------------------------------------------------------------#

    def clearAll(self, *args):
        for interp_widget in self._interp_widgets:
            interp_widget.clearItems()

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
    def __init__(self):
        qg.QFrame.__init__(self)
        self.setFrameStyle(qg.QFrame.Panel | qg.QFrame.Raised)

        self.setLayout(qg.QVBoxLayout())
        self.layout().setContentsMargins(3,1,3,3)
        self.layout().setSpacing(0)
        self.setFixedHeight(150)

        main_widget = qg.QWidget()
        main_widget.setLayout(qg.QVBoxLayout())
        main_widget.layout().setContentsMargins(2,2,2,2)
        main_widget.layout().setSpacing(5)
        main_widget.setFixedHeight(140)
        main_widget.setFixedWidth(290)

        graphics_scene = qg.QGraphicsScene()
        graphics_view  = qg.QGraphicsView()
        graphics_view.setScene(graphics_scene)
        graphics_view.setHorizontalScrollBarPolicy(qc.Qt.ScrollBarAlwaysOff)
        graphics_view.setVerticalScrollBarPolicy(qc.Qt.ScrollBarAlwaysOff)
        graphics_view.setFocusPolicy(qc.Qt.NoFocus)
        graphics_view.setSizePolicy(qg.QSizePolicy.Minimum, qg.QSizePolicy.Minimum)
        graphics_view.setStyleSheet("QGraphicsView {border-style: none;}")
        self.layout().addWidget(graphics_view)
        self.main_widget_proxy = graphics_scene.addWidget(main_widget)
        main_widget.setParent(graphics_view)

        title_layout  = qg.QHBoxLayout()
        select_layout = qg.QHBoxLayout()
        button_layout = qg.QHBoxLayout()
        slider_layout = qg.QHBoxLayout()
        check_layout  = qg.QHBoxLayout()
        main_widget.layout().addLayout(title_layout)
        main_widget.layout().addLayout(select_layout)
        main_widget.layout().addLayout(button_layout)
        main_widget.layout().addLayout(slider_layout)
        main_widget.layout().addLayout(check_layout)

        title_line = DT_LineEdit()
        title_line.setPlaceholderMessage('Untitled')
        title_layout.addWidget(title_line)

        self.close_bttn = DT_CloseButton('X')
        self.close_bttn.setObjectName('roundedButton')
        title_layout.addWidget(self.close_bttn)

        store_items = DT_Button('Store Items')
        clear_items = DT_Button('Clear Items')

        select_layout.addSpacerItem(qg.QSpacerItem(5, 5, qg.QSizePolicy.Expanding))
        select_layout.addWidget(store_items)
        select_layout.addWidget(clear_items)
        select_layout.addSpacerItem(qg.QSpacerItem(5, 5, qg.QSizePolicy.Expanding))

        self.store_start_bttn = DT_ButtonThin('Store Start')
        self.reset_item_bttn  = DT_ButtonThin('Reset')
        self.store_end_bttn   = DT_ButtonThin('Store End')

        button_layout.addWidget(self.store_start_bttn)
        button_layout.addWidget(self.reset_item_bttn)
        button_layout.addWidget(self.store_end_bttn)

        self.start_lb = DT_Label('Start')
        self.slider = DT_Slider()
        self.slider.setRange(0, 49)
        self.end_lb = DT_Label('End')

        slider_layout.addWidget(self.start_lb)
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.end_lb)

        self.transforms_chbx = DT_Checkbox('Transform')
        self.attributes_chbx = DT_Checkbox('UD Attributes')
        self.transforms_chbx.setCheckState(qc.Qt.Checked)
        check_layout.addWidget(self.transforms_chbx)
        check_layout.addWidget(self.attributes_chbx)

        self.items = {}
        self.slider_down = False
        self._animation = None

        self.close_bttn.clicked.connect(self.closeWidget)

        store_items.clicked.connect(self.storeItems)
        clear_items.clicked.connect(self.clearItems)

        self.store_start_bttn.clicked.connect(self.storeStart)
        self.store_end_bttn.clicked.connect(self.storeEnd)
        self.reset_item_bttn.clicked.connect(self.resetAttributes)

        self.slider.valueChanged.connect(self.setLinearInterpolation)
        self.slider.valueChanged.connect(self.changeLabelGlow)

        self.slider.sliderReleased.connect(self._endSliderUndo)

        self.enableButtons(False)

    #------------------------------------------------------------------------------------------#

    def _animateExpand(self, value):
        opacity_anim = qc.QPropertyAnimation(self.main_widget_proxy, "opacity")
        opacity_anim.setStartValue(not(value));
        opacity_anim.setEndValue(value)
        opacity_anim.setDuration(200)
        opacity_anim_curve = qc.QEasingCurve()
        if value is True:
            opacity_anim_curve.setType(qc.QEasingCurve.InQuad)
        else:
            opacity_anim_curve.setType(qc.QEasingCurve.OutQuad)
        opacity_anim.setEasingCurve(opacity_anim_curve)

        size_anim = qc.QPropertyAnimation(self, "geometry")

        geometry = self.geometry()
        width    = geometry.width()
        x, y, _, _ = geometry.getCoords()

        size_start = qc.QRect(x, y, width, int(not(value)) * 150)
        size_end   = qc.QRect(x, y, width, value * 150)

        size_anim.setStartValue(size_start)
        size_anim.setEndValue(size_end)
        size_anim.setDuration(300)

        size_anim_curve = qc.QEasingCurve()
        if value:
            size_anim_curve.setType(qc.QEasingCurve.InQuad)
        else:
            size_anim_curve.setType(qc.QEasingCurve.OutQuad)
        size_anim.setEasingCurve(size_anim_curve)

        self._animation = qc.QSequentialAnimationGroup()
        if value:
            self.main_widget_proxy.setOpacity(0)
            self._animation.addAnimation(size_anim)
            self._animation.addAnimation(opacity_anim)
        else:
            self.main_widget_proxy.setOpacity(1)
            self._animation.addAnimation(opacity_anim)
            self._animation.addAnimation(size_anim)

        size_anim.valueChanged.connect(self._forceResize)
        self._animation.finished.connect(self._animation.clear)

        if not value:
            self._animation.finished.connect(self.deleteWidget)

        self._animation.start(qc.QAbstractAnimation.DeleteWhenStopped)


    def _forceResize(self, new_height):
        self.setFixedHeight(new_height.toRect().height())

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
            return

        self.items = {}
        for node in selection:
            self.items[node.name()] = {NODE:node, START:{}, END:{}, CACHE:{}}

        self.enableButtons(True)


    def clearItems(self):
        self.items = {}
        self.enableButtons(False)
        self.slider.setValue(0)

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


    def hideCloseButton(self, value=True):
        self.close_bttn.setVisible(not(value))

    #------------------------------------------------------------------------------------------#

    def storeStart(self):
        if not self.items: return
        self._store(START, 0)
        self._cache()
        self.changeLabelGlow(0)


    def storeEnd(self):
        if not self.items: return
        self._store(END, 50)
        self._cache()
        self.changeLabelGlow(49)


    def _store(self, key, value):
        for name, item_dict in self.items.items():
            node = item_dict[NODE]

            if not node.exists():
                del(self.items[name])
                continue

            attrs = self.getAttributes(node)
            data = item_dict[key]
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
                    interval     = float(end_attr - start_attr) / 49.0
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
                if attr.type() not in ('double', 'int'): continue
                if attr.isLocked(): continue

                attrs.append(attr.name().split('.')[-1])

        return attrs


    @undo_pm
    def resetAttributes(self, *args):
        if not self.items:
            return

        for name, item_dict in self.items.items():
            node = item_dict[NODE]

            if not node.exists():
                del(self.items[name])
                continue

            attrs = self.getAttributes(node)

            for attr in attrs:
                default_value = pm.attributeQuery(attr, node=node, ld=True)[0]
                node.attr(attr).set(default_value)

    #------------------------------------------------------------------------------------------#

    def setLinearInterpolation(self, value):
        if not self.items: return

        if not self.slider_down:
            self._startSliderUndo()
            self.slider_down = True

        for name, item_dict in self.items.items():
            node  = item_dict[NODE]
            start = item_dict[START]

            if not node.exists():
                del(self.items[name])
                continue

            if not start or not item_dict[END]: continue

            cache = item_dict[CACHE]

            for attr in cache.keys():
                if cache[attr] == None: continue
                pm.setAttr(node.attr(attr), cache[attr][value])


    def changeLabelGlow(self, value):
        glow_value = int(float(value) / self.slider.maximum() * 100)
        self.start_lb.setGlowValue(100 - glow_value)
        self.end_lb.setGlowValue(glow_value)


    def closeWidget(self):
        self.emit(qc.SIGNAL('CLOSE'), self)

    def deleteWidget(self):
        self.emit(qc.SIGNAL('DELETE'), self)

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

        widget = mui.MQtUtil.findControl(dock)
        dock_widget = sip.wrapinstance(long(widget), qc.QObject)
        dialog.connectDockWidget(dock, dock_widget)

    else:
        dialog.show()


def delete():
    global dialog
    if dialog:
        dialog.close()
        dialog = None
