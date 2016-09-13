import PyQt4.QtCore as qc
import PyQt4.QtGui as qg


class DT_Button(qg.QPushButton):
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

        painter.setPen(qg.QPen(qg.QColor(0,255,0), 3, qc.Qt.SolidLine))
        painter.setBrush(qg.QBrush(qg.QColor(255, 0, 0)))
        painter.drawRoundedRect(qc.QRect(x+1, y+1, width-1, height-1), 5, 5)

        text = self.text()
        painter.setPen(qg.QPen(qg.QColor(0, 0, 255)))
        painter.drawText(x, y, width, height, (qc.Qt.AlignHCenter | qc.Qt.AlignVCenter), text)
