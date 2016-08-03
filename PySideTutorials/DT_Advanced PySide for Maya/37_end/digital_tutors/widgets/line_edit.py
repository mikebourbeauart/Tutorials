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



    def setPlaceholderMessage(self, message):
        self._placeholder_message = str(message)



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
