import PyQt4.QtCore as qc
import PyQt4.QtGui as qg

from PyQt4.QtGui import QPen, QColor, QBrush, QLinearGradient

import maya.utils as utils

import base

#--------------------------------------------------------------------------------------------------#

class DT_Slider(qg.QSlider, base.Base):
    _pens_dark  = QPen(QColor( 0,  5,  9), 1, qc.Qt.SolidLine)
    _pens_light = QPen(QColor(16, 17, 19), 1, qc.Qt.SolidLine)

    _gradient_inner = QLinearGradient(0, 9, 0, 15)
    _gradient_inner.setColorAt(0, QColor(69, 73, 76))
    _gradient_inner.setColorAt(1, QColor(17, 18, 20))

    _gradient_outer = QLinearGradient(0, 9, 0, 15)
    _gradient_outer.setColorAt(0, QColor(53, 57, 60))
    _gradient_outer.setColorAt(1, QColor(33, 34, 36))


    def __init__(self, *args, **kwargs):
        qg.QSlider.__init__(self, *args, **kwargs)
        base.Base.__init__(self)

        self.setOrientation(qc.Qt.Horizontal)
        self.setFixedHeight(22)
        self.setMinimumWidth(50)

    #-----------------------------------------------------------------------------------------#

    def paintEvent(self, event):
        painter = qg.QStylePainter(self)
        option  = qg.QStyleOption()
        option.initFrom(self)

        x = option.rect.x()
        y = option.rect.y()
        height = option.rect.height() - 1
        width  = option.rect.width()  - 1

        orientation = self.orientation()

        painter.setRenderHint(qg.QPainter.Antialiasing)

        painter.setPen(self._pens_shadow)
        painter.setBrush(self._brush_border)
        painter.drawRoundedRect(qc.QRect(x+1, y+1, width-1, height-1), 10, 10)

        mid_height = (height / 2) + 1
        painter.setPen(self._pens_dark)
        painter.drawLine(10, mid_height, width - 8, mid_height)
        painter.setRenderHint(qg.QPainter.Antialiasing, False)
        painter.setPen(self._pens_light)
        painter.drawLine(10, mid_height, width - 10, mid_height)
        painter.setRenderHint(qg.QPainter.Antialiasing, True)

        minimum     = self.minimum()
        maximum     = self.maximum()
        value_range = maximum - minimum
        value       = self.value() - minimum

        increment = ((width - 20) / float(value_range))
        center = 10 + (increment * value)
        center_point = qc.QPoint(x + center, y + mid_height)

        painter.setPen(self._pens_clear)

        painter.setBrush(qg.QBrush(self._gradient_outer))
        painter.drawEllipse(center_point, 6, 6)

        painter.setBrush(qg.QBrush(self._gradient_inner))
        painter.drawEllipse(center_point, 5, 5)
