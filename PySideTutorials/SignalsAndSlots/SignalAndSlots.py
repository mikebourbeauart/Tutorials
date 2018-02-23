import sys
from Qt import QtWidgets
from Qt import QtCore


class MainWidget(QtWidgets.QDialog):

	speak = QtCore.Signal()

	def __init__(self, parent=None):
		super(MainWidget, self).__init__(parent)

		button = QtWidgets.QPushButton("Call someFunc")
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.main_layout.addWidget(button)
		self.setLayout(self.main_layout)

		button.clicked.connect(self.speakingMethod)
		self.speak.connect(self.hey_there)
	def speakingMethod(self):
		self.speak.emit()

	def hey_there(self):
		print 'hey there'

class ButtonWidget(QtWidgets.QPushButton):
	def __init__(self, parent=None):
		super(ButtonWidget, self).__init__(parent)



def main():

	app = QtWidgets.QApplication(sys.argv)
	window = MainWidget()
	window.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()