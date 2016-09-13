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
        self.setFixedHeight(27)

        self._radius = 5

        self.font_metrics = qg.QFontMetrics(self.font())



    def paintEvent(self, event):
        painter = qg.QStylePainter(self)
        option  = qg.QStyleOption()
        option.initFrom(self)

        x = option.rect.x()
        y = option.rect.y()
        height = option.rect.height() - 1
        width  = option.rect.width()  - 1

        painter.setRenderHint(qg.QPainter.Antialiasing)

        radius = self._radius

        gradient = self._gradient[NORMAL]
        offset = 0
        if self.isDown():
            gradient = self._gradient[DOWN]
            offset = 1
        elif not self.isEnabled():
            gradient = self._gradient[DISABLED]

        painter.setBrush(self._brush_border)
        painter.setPen(self._pens_border)
        painter.drawRoundedRect(qc.QRect(x+1, y+1, width-1, height-1), radius, radius)

        painter.setPen(self._pens_clear)

        painter.setBrush(gradient[OUTER])
        painter.drawRoundedRect(qc.QRect(x+2, y+2, width-3, height-3), radius, radius)

        painter.setBrush(gradient[INNER])
        painter.drawRoundedRect(qc.QRect(x+3, y+3, width-5, height-5), radius-1, radius-1)

        # draw text
        #
        text = self.text()
        font = self.font()

        text_width  = self.font_metrics.width(text)
        text_height = font.pointSize()

        text_path = qg.QPainterPath()
        text_path.addText((width-text_width)/2, height-((height-text_height)/2) - 1 + offset, font, text)

        alignment = (qc.Qt.AlignHCenter | qc.Qt.AlignVCenter)

        if self.isEnabled():
            painter.setPen(self._pens_shadow)
            painter.drawPath(text_path)

            painter.setPen(self._pens_text)
            painter.drawText(x, y+offset, width, height, alignment, text)
        else:
            painter.setPen(self._pens_shadow_disabled)
            painter.drawPath(text_path)

            painter.setPen(self._pens_text_disabled)
            painter.drawText(x, y+offset, width, height, alignment, text)

#--------------------------------------------------------------------------------------------------#

class DT_ButtonThin(DT_Button):
    def __init__(self, *args, **kwargs):
        DT_Button.__init__(self, *args, **kwargs)
        self._radius = 10
        self.setFixedHeight(22)

#--------------------------------------------------------------------------------------------------#

class DT_CloseButton(DT_Button):
    def __init__(self, *args, **kwargs):
        DT_Button.__init__(self, *args, **kwargs)
        self._radius = 10
        self.setFixedHeight(20)
        self.setFixedWidth(20)


    def paintEvent(self, event):
        painter = qg.QStylePainter(self)
        option  = qg.QStyleOption()
        option.initFrom(self)

        x = option.rect.x()
        y = option.rect.y()
        height = option.rect.height() - 1
        width  = option.rect.width()  - 1

        painter.setRenderHint(qg.QPainter.Antialiasing)

        gradient = self._gradient[NORMAL]
        offset = 0
        if self.isDown():
            gradient = self._gradient[DOWN]
            offset = 1
        elif not self.isEnabled():
            gradient = self._gradient[DISABLED]

        painter.setPen(self._pens_border)
        painter.drawEllipse(x+1, y+1, width-1, height-1)

        painter.setPen(self._pens_clear)
        painter.setBrush(gradient[OUTER])
        painter.drawEllipse(x+2, y+2, width-3, height-2)

        painter.setBrush(gradient[INNER])
        painter.drawEllipse(x+3, y+3, width-5, height-4)

        painter.setBrush(self._brush_clear)

        line_path = qg.QPainterPath()
        line_path.moveTo( x+8,  y+8)
        line_path.lineTo(x+12, x+12)
        line_path.moveTo(x+12,  y+8)
        line_path.lineTo( x+8, y+12)

        painter.setPen(self._pens_border)
        painter.drawPath(line_path)
