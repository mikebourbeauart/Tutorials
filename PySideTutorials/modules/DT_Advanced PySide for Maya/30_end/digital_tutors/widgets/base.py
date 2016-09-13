import PyQt4.QtCore as qc
import PyQt4.QtGui as qg

import maya.utils as utils


class Base(object):
    def __init__(self):
        font = qg.QFont()
        font.setPointSize(8)
        font.setFamily("Calibri")
        self.setFont(font)

        self._hover = False
        self._glow_index = 0
        self._anim_timer = qc.QTimer()
        self._anim_timer.timeout.connect(self._animateGlow)



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
