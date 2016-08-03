import sys

from PySide import QtGui
from PySide import QtCore


if __name__ == "__main__":

	 
	base = QtGui.QPixmap('S:/_management/_mb_Pipeline/mb_Armada/mb_Armada/assets/icons/mb_MBP_message.png')

	overlay = QtGui.QPixmap(
		'S:/_management/_mb_Pipeline/mb_Armada/mb_Armada/assets/icons/mb_MBP_backArrow.png')

	point = QtCore.QPoint(0, 0)
	painter = QtGui.QPainter(base)
	painter.drawPixmap(point, overlay)
		

	label = QtGui.QLabel()
	label.setPixmap(QtGui.QPixmap.fromImage(image))
	label.show()

	app = QtGui.QApplication(sys.argv)
	sys.exit(app.exec_())