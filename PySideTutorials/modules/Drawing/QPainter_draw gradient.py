from PySide import QtGui 
from PySide import QtCore 

import sys

class Example(QtGui.QWidget):
	
	def __init__(self):
		super(Example, self).__init__()

		self.initUI()
		
	def initUI(self):      

		self.setGeometry(300, 300, 280, 170)
		self.setWindowTitle('Gradient')
		self.show()

		def paintEvent(self, event):

			pixmap	= QtGui.QPixmap (QtCore.QSize(400,400))    
			painter	= QtGui.QPainter (pixmap)   
			painter.begin(self)
			self.drawPoints(painter)
			painter.end()

			gradient = QtGui.QLinearGradient(
				QtCore.QPointF(pixmap.rect().topLeft()),
				QtCore.QPointF(pixmap.rect().bottomLeft())
			)
		
			gradient.setColorAt(0, QtCore.Qt.blue)
			gradient.setColorAt(0.4, QtCore.Qt.cyan)
			gradient.setColorAt(1, QtCore.Qt.green)    
		
			brush 	= QtGui.QBrush(gradient)        
			painter.fillRect( QtCore.QRectF(0, 0, 400, 400),brush)
			painter.drawText( QtCore.QRectF(0, 0, 400, 400),
					  QtCore.Qt.AlignCenter, 
					  "This is an image created with QPainter and QPixmap")
			  
		#pixmap.save("/home/developer/output.jpg")     
		
def main():
	
	app = QtGui.QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()