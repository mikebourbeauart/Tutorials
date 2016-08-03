from PySide import QtCore, QtGui
from shiboken import wrapInstance 
import maya.OpenMayaUI as mui


def get_parent():
	ptr = mui.MQtUtil.mainWindow()
	return wrapInstance( long( ptr ), QtGui.QWidget )   

class MainWindow(QtGui.QDialog):
	def __init__( self, parent=get_parent() ):
		super( MainWindow, self ).__init__( parent )

		self.layout=QtGui.QVBoxLayout()
		self.setLayout(self.layout)


		self.checkbox=QtGui.QCheckBox("Layouts")
		self.layout.addWidget(self.checkbox)


		self.widget1=QtGui.QWidget()
		self.layout.addWidget(self.widget1)

		self.layout1=QtGui.QVBoxLayout()
		self.widget1.setLayout(self.layout1)

		self.layout1.addWidget(QtGui.QLabel("First layout"))

		self.layout1.addWidget(QtGui.QTextEdit())


		self.widget2=QtGui.QWidget()
		self.layout.addWidget(self.widget2)

		self.layout2=QtGui.QHBoxLayout()
		self.widget2.setLayout(self.layout2)

		self.layout2.addWidget(QtGui.QTextEdit("Second layout"))

		self.layout2.addWidget(QtGui.QTextEdit())


		self.checkbox.toggled.connect(self.checkbox_toggled)
		self.checkbox.toggle()

		self.show()

	def checkbox_toggled(self, state):
		self.widget1.setVisible(state)
		self.widget2.setVisible(not state)

try:
	mw.close()
	mw.deleteLater()
except:
	pass

# Action stuff
mw = MainWindow()
mw.show()

# Development stuff
try:
	mw.show()
except:
	mw.close()
	mw.deleteLater()

