import PyQt4.QtCore as qc
import PyQt4.QtGui as qg

import maya.utils as utils

import base

#--------------------------------------------------------------------------------------------------#

class DT_LineEdit(qg.QLineEdit):
    _glow_pens = base.Base._glow_pens

    _pens_text   = base.Base._pens_text
    _pens_shadow = base.Base._pens_shadow
    _pens_border = base.Base._pens_border
    _pens_clear  = base.Base._pens_clear

    _brush_clear = base.Base._brush_clear

    _pens_placeholder = qg.QPen(qg.QColor(202, 207, 210, 127), 1, qc.Qt.SolidLine)


    def __init__(self, *args, **kwargs):
        qg.QLineEdit.__init__(self, *args, **kwargs)

        font = qg.QFont()
        font.setPixelSize(16)
        self.setFont(font)
        self.font_metrics = qg.QFontMetrics(font)
        self.setFixedHeight(self.font_metrics.height() + 7)

        self._placeholder_message = ''

        self._text_glow = {}
        self._previous_text = ''

        text = self.text()
        if text: self.setText(text)

        self._anim_timer = qc.QTimer()

    #------------------------------------------------------------------------------------------#

    def setText(self, *args):
        qg.QLineEdit.setText(self, *args)
        self._text_glow = {}
        for index in range(len(text)):
            self._text_glow[index] = 0


    def setPlaceholderMessage(self, message):
        self._placeholder_message = str(message)

    #------------------------------------------------------------------------------------------#

    def keyPressEvent(self, *args):
        qg.QLineEdit.keyPressEvent(self, *args)
        text = self.text()

        if text == self._previous_text: return

        len_text = len(text)
        if len_text > len(self._previous_text):
            self._anim_timer.start(30)
            self._text_glow[len_text-1] = 0
            self._text_glow[self.cursorPosition()-1] = 10

        elif len(self._text_glow.keys()) == 0:
            self._anim_timer.stop()

        self._previous_text = text

        print self._text_glow

    #------------------------------------------------------------------------------------------#

    def paintEvent(self, event):
        painter = qg.QStylePainter(self)
        option  = qg.QStyleOptionFrame()
        self.initStyleOption(option)

        painter.setRenderHint(qg.QPainter.Antialiasing)
        painter.setRenderHint(qg.QPainter.TextAntialiasing)

        contents = self.style().subElementRect(qg.QStyle.SE_LineEditContents, option, self)
        contents.setLeft(contents.left() + 2)
        contents.setRight(contents.right() - 2)
        alignment = (qc.Qt.AlignLeft | qc.Qt.AlignVCenter)

        text = self.text()
        font = self.font()
        font_metrics = self.font_metrics

        if not text:
            painter.setPen(self._pens_placeholder)
            painter.drawText(contents, alignment, self._placeholder_message)

        x, y, width, height = contents.getRect()

        painter.setPen(self._pens_shadow)
        painter.drawText(x+1, y+1, width, height, alignment, text)
        painter.setPen(self._pens_text)
        painter.drawText(contents, alignment, text)

        cursor_pos = self.cursorPosition()
        text_width = font_metrics.width(text[0:cursor_pos])
        pos  = x + text_width
        top  = y + 1
        bttm = y + height - 1
        painter.drawLine(pos, top, pos, bttm)
