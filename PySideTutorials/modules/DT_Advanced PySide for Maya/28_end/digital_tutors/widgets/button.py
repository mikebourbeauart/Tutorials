import PyQt4.QtCore as qc
import PyQt4.QtGui as qg

from PyQt4.QtGui import QPen, QColor, QBrush, QLinearGradient

NORMAL, DOWN, DISABLED = 1, 2, 3
INNER, OUTER = 1, 2


class DT_Button(qg.QPushButton):
    _pens_text   = QPen(qg.QColor(202, 207, 210), 1, qc.Qt.SolidLine)
    _pens_shadow = QPen(qg.QColor(  9,  10,  12), 1, qc.Qt.SolidLine)
    _pens_border = QPen(qg.QColor(  9,  10,  12), 2, qc.Qt.SolidLine)
    _pens_clear  = QPen(qg.QColor(  0,  0, 0, 0), 1, qc.Qt.SolidLine)

    _pens_text_disabled   = QPen(QColor(102, 107, 110), 1, qc.Qt.SolidLine)
    _pens_shadow_disabled = QPen(QColor(  0,   0,   0), 1, qc.Qt.SolidLine)

    _brush_clear  = QBrush(qg.QColor(0, 0, 0, 0))
    _brush_border = QBrush(qg.QColor( 9, 10, 12))

    _gradient = {NORMAL:{}, DOWN:{}, DISABLED:{}}

    inner_gradient = QLinearGradient(0, 3, 0, 24)
    inner_gradient.setColorAt(0, QColor(53, 57, 60))
    inner_gradient.setColorAt(1, QColor(33, 34, 36))
    _gradient[NORMAL][INNER] = QBrush(inner_gradient)

    outer_gradient = QLinearGradient(0, 2, 0, 25)
    outer_gradient.setColorAt(0, QColor(69, 73, 76))
    outer_gradient.setColorAt(1, QColor(17, 18, 20))
    _gradient[NORMAL][OUTER] = QBrush(outer_gradient)

    inner_gradient_down = QLinearGradient(0, 3, 0, 24)
    inner_gradient_down.setColorAt(0, QColor(20, 21, 23))
    inner_gradient_down.setColorAt(1, QColor(48, 49, 51))
    _gradient[DOWN][INNER] = QBrush(inner_gradient_down)

    outer_gradient_down = QLinearGradient(0, 2, 0, 25)
    outer_gradient_down.setColorAt(0, QColor(36, 37, 39))
    outer_gradient_down.setColorAt(1, QColor(32, 33, 35))
    _gradient[DOWN][OUTER] = QBrush(outer_gradient_down)

    inner_gradient_disabled = QLinearGradient(0, 3, 0, 24)
    inner_gradient_disabled.setColorAt(0, QColor(33, 37, 40))
    inner_gradient_disabled.setColorAt(1, QColor(13, 14, 16))
    _gradient[DISABLED][INNER] = QBrush(inner_gradient_disabled)

    outer_gradient_disabled = QLinearGradient(0, 2, 0, 25)
    outer_gradient_disabled.setColorAt(0, QColor(49, 53, 56))
    outer_gradient_disabled.setColorAt(1, QColor( 9, 10, 12))
    _gradient[DISABLED][OUTER] = QBrush(outer_gradient_disabled)



    def __init__(self, *args, **kwargs):
        qg.QPushButton.__init__(self, *args, **kwargs)



    def paintEvent(self, event):
        painter = qg.QStylePainter(self)
        option  = qg.QStyleOption()
        option.initFrom(self)

        x = option.rect.x()
        y = option.rect.y()
        height = option.rect.height() - 1
        width  = option.rect.width()  - 1

        painter.setRenderHint(qg.QPainter.Antialiasing)

        radius = 5

        gradient = self._gradient[NORMAL]
        offset = 0
        if self.isDown():
            gradient = self._gradient[DOWN]
            offset = 1
        elif not self.isEnabled():
            gradient = self._gradient[DISABLED]

        painter.setBrush(gradient[OUTER])
        painter.drawRoundedRect(qc.QRect(x+2, y+2, width-3, height-3), radius, radius)

        painter.setBrush(gradient[INNER])
        painter.drawRoundedRect(qc.QRect(x+3, y+3, width-5, height-5), radius-1, radius-1)
