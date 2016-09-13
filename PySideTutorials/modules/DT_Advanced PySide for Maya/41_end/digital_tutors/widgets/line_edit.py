import PyQt4.QtCore as qc
import PyQt4.QtGui as qg

import maya.utils as utils

import base


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
        self._anim_timer.timeout.connect(self._animateText)


    def setText(self, *args):
        qg.QLineEdit.setText(self, *args)
        self._text_glow = {}
        for index in range(len(text)):
            self._text_glow[index] = 0


    def setPlaceholderMessage(self, text):
        self._placeholder_message = str(text)



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



    def _animateText(self):
        stop_animating = True
        for key, value in self._text_glow.items():
            if value > 0:
                stop_animating = False
                self._text_glow[key] = value - 1

        if stop_animating:
            self._anim_timer.stop()

        utils.executeDeferred(self.update)



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

        glow_pens  = self._glow_pens

        selected = self.hasSelectedText()
        if selected:
            selection = self.selectedText()
            selection_start = self.selectionStart()
            selection_end = selection_start + len(selection)

        left_edge = contents.left()
        for index, letter in enumerate(text):
            text_width = font_metrics.width(text[0:index])
            contents.setLeft(left_edge + text_width)

            x, y, width, height = contents.getRect()

            painter.setPen(self._pens_shadow)
            painter.drawText(x+1, y+1, width, height, alignment, letter)
            painter.setPen(self._pens_text)
            painter.drawText(contents, alignment, letter)

            glow_index = self._text_glow[index]
            if selected and (index >= selection_start and index < selection_end):
                glow_index = 10

            if glow_index > 0:
                text_path = qg.QPainterPath()
                text_path.addText(contents.left(), font.pixelSize() + 4, font, letter)

                for index in range(3):
                    painter.setPen(glow_pens[glow_index][index])
                    painter.drawPath(text_path)

                painter.setPen(glow_pens[glow_index][3])
                painter.drawText(contents, alignment, letter)


        if not self.hasFocus(): return

        contents.setLeft(left_edge)
        x, y, width, height = contents.getRect()

        painter.setPen(self._pens_text)

        cursor_pos = self.cursorPosition()
        text_width = font_metrics.width(text[0:cursor_pos])
        pos = x + text_width
        top = y + 1
        bttm = y + height - 1
        painter.drawLine(pos, top, pos, bttm)

        try:
            cursor_glow = self._text_glow[cursor_pos-1]
        except KeyError:
            return

        if cursor_glow > 0:
            for index in range(4):
                painter.setPen(glow_pens[cursor_glow][index])
                painter.drawLine(pos, top, pos, bttm)
