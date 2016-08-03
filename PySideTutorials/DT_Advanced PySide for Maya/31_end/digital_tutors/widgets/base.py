import PyQt4.QtCore as qc
import PyQt4.QtGui as qg

import maya.utils as utils

from PyQt4.QtGui import QPen, QColor, QBrush, QLinearGradient


class Base(object):
    _glow_pens = {}
    for index in range(1, 11):
        _glow_pens[index] = [QPen(QColor(0, 255, 0, 12   * index), 1, qc.Qt.SolidLine),
                             QPen(QColor(0, 255, 0,  5   * index), 3, qc.Qt.SolidLine),
                             QPen(QColor(0, 255, 0,  2   * index), 5, qc.Qt.SolidLine),
                             QPen(QColor(0, 255, 0, 25.5 * index), 1, qc.Qt.SolidLine)]

    _pens_text   = QPen(qg.QColor(202, 207, 210), 1, qc.Qt.SolidLine)
    _pens_shadow = QPen(qg.QColor(  9,  10,  12), 1, qc.Qt.SolidLine)
    _pens_border = QPen(qg.QColor(  9,  10,  12), 2, qc.Qt.SolidLine)
    _pens_clear  = QPen(qg.QColor(  0,  0, 0, 0), 1, qc.Qt.SolidLine)

    _pens_text_disabled   = QPen(QColor(102, 107, 110), 1, qc.Qt.SolidLine)
    _pens_shadow_disabled = QPen(QColor(  0,   0,   0), 1, qc.Qt.SolidLine)

    _brush_clear  = QBrush(qg.QColor(0, 0, 0, 0))
    _brush_border = QBrush(qg.QColor( 9, 10, 12))

    def __init__(self):
        font = qg.QFont()
        font.setPointSize(8)
        font.setFamily("Calibri")
        self.setFont(font)

        self._hover = False
        self._glow_index = 0
        self._anim_timer = qc.QTimer()
        self._anim_timer.timeout.connect(self._animateGlow)

    #-----------------------------------------------------------------------------------------#

    def _animateGlow(self):
        if self._hover:
            if self._glow_index >= 10:
                self._glow_index = 10
                self._anim_timer.stop()
            else:
                self._glow_index += 1

        else:
            if self._glow_index <= 0:
                self._glow_index = 0
                self._anim_timer.stop()
            else:
                self._glow_index -= 1

        utils.executeDeferred(self.update)

    #-----------------------------------------------------------------------------------------#

    def enterEvent(self, event):
        super(self.__class__, self).enterEvent(event)

        if not self.isEnabled(): return

        self._hover = True
        self._startAnim()


    def leaveEvent(self, event):
        super(self.__class__, self).leaveEvent(event)

        if not self.isEnabled(): return

        self._hover = False
        self._startAnim()


    def _startAnim(self):
        if self._anim_timer.isActive():
            return

        self._anim_timer.start(20)
