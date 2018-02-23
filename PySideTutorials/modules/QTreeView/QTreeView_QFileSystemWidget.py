from Qt import QtGui
from Qt import QtCore

def someFunc():
	print "someFunc has been called!"

button = QtWidgets.QPushButton("Call someFunc")
QtCore.QObject.connect(button, QtCore.SIGNAL ('clicked()'), someFunc)