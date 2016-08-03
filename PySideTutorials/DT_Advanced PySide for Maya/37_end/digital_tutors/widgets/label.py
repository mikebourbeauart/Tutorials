import PyQt4.QtCore as qc
import PyQt4.QtGui as qg

import maya.utils as utils

import base

#--------------------------------------------------------------------------------------------------#

class DT_Label(qg.QLabel):
    _glow_pens = base.Base._glow_pens

    _pens_text   = base.Base._pens_text
    _pens_shadow = base.Base._pens_shadow

    _pens_text_disabled   = base.Base._pens_text_disabled
    _pens_shadow_disabled = base.Base._pens_shadow_disabled


    def __init__(self, *args, **kwargs):
        qg.QLabel.__init__(self, *args, **kwargs)

        font = qg.QFont()
        font.setFamily("Calibri")
        font.setPointSize(8)
        self.setFont(font)

        self.setMargin(3)
        self._glow_index = 0

    #------------------------------------------------------------------------------------------#

    def setGlowValue(self, value):
        self._glow_index = min(max(value / 10, 0), 10)
        utils.executeDeferred(self.update)

    #------------------------------------------------------------------------------------------#

    def paintEvent(self, event):
        painter = qg.QStylePainter(self)
        option  = qg.QStyleOption()
        option.initFrom(self)

        x = option.rect.x()
        y = option.rect.y()
        height = option.rect.height() - 1
        width  = option.rect.width()  - 1

        painter.setRenderHint(qg.QPainter.Antialiasing)
        painter.setRenderHint(qg.QPainter.TextAntialiasing)

        font = self.font()
        text = self.text()
        if text == '': return

        font_metrics = qg.QFontMetrics(font)
        text_width  = font_metrics.width(text)
        text_height = font.pointSize()

        text_path = qg.QPainterPath()
        text_path.addText((width-text_width)/2, height-((height-text_height)/2) - 1, font, text)

        alignment = (qc.Qt.AlignHCenter | qc.Qt.AlignVCenter)

        if self.isEnabled():
            pens_text   = self._pens_text
            pens_shadow = self._pens_shadow
        else:
            pens_text   = self._pens_text_disabled
            pens_shadow = self._pens_shadow_disabled

        painter.setPen(pens_shadow)
        painter.drawPath(text_path)
        painter.setPen(pens_text)
        painter.drawText(x, y, width, height, alignment, text)

        glow_index = self._glow_index
        glow_pens  = self._glow_pens

        if glow_index > 0:
            for index in range(3):
                painter.setPen(glow_pens[glow_index][index])
                painter.drawPath(text_path)

            painter.setPen(glow_pens[glow_index][3])
            painter.drawText(x, y, width, height, alignment, text)
