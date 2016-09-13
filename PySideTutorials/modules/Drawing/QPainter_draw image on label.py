from PySide import QtGui
from PySide import QtCore
import sys

class Example(QtGui.QWidget):
	def __init__(self):
		super(Example, self).__init__()

		self.initUI()

	def initUI(self):    
		  
		hbox = QtGui.QHBoxLayout(self)
		self.lbl = MyLabel(self)
		hbox.addWidget(self.lbl)
		self.setLayout(hbox)
		self.show()
	

class MyLabel(QtGui.QLabel):
	def __init__(self, parent):
		super(MyLabel, self).__init__()

		self.setMouseTracking(True)
		self.setAttribute(QtCore.Qt.WA_PaintOutsidePaintEvent)

		self.icon_pixmap = QtGui.QPixmap(
			'D:/Git_Stuff/Tutorials/PySideTutorials/_TestImages/ftrack_create_asset.png'
		)

		self.overlay_pixmap = QtGui.QPixmap(
			'D:/Git_Stuff/Tutorials/PySideTutorials/_TestImages/ftrack_connect_play.png'
		)
		
		self.setPixmap(self.icon_pixmap)



	def enterEvent(self, event):
		pixmap_base = QtGui.QPixmap()
		pixmap_base.fill(QtCore.Qt.transparent)
		painter = QtGui.QPainter(self)
		painter.begin(self.icon_pixmap)
		painter.drawPixmap(0, 0, self.width(), self.height(), self.icon_pixmap)
		painter.drawPixmap(0, 0, self.width(), self.height(), self.overlay_pixmap)
		painter.end()

		self.setPixmap(pixmap_base)
		

def main():
	
	app = QtGui.QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()