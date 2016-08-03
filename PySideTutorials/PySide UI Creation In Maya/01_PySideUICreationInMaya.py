from PySide import QtGui
import maya.OpenMayaUI as mui
import shiboken
import maya.cmds as mc

def getMayaWindow():
    pointer = mui.MQtUtil.mainWindow()
    return shiboken.wrapInstance( long(pointer), QtGui.QWidget )

def createLocator():
    mc.spaceLocator()

objectName = "pyMyWin"

# Check for existing window
if mc.window("pyMyWin", exists=True):
    mc.deleteUI("pyMyWin", wnd=True)

# Create a window
parent = getMayaWindow()
window = QtGui.QMainWindow(parent)
window.setObjectName(objectName)

# Create a font
font = QtGui.QFont()
font.setPointSize( 12 )
font.setBold( True )

# Create a widget
widget = QtGui.QWidget()
window.setCentralWidget(widget)

# Create a layout
layout = QtGui.QVBoxLayout(widget)

# Create the button
button = QtGui.QPushButton( "Create Locator" )
layout.addWidget(button)
button.setFont( font )
button.setMinimumSize( 200, 40 )
button.setMaximumSize( 200, 40 )
imagePath = mc.internalVar( upd=True ) + "icons/blue_field_background.png"
button.setStyleSheet( "background-image: url( " + imagePath + " ) ; border: solid black 1px" )
button.clicked.connect(createLocator)

# Create close button
closeButton = QtGui.QPushButton("Close")
layout.addWidget(closeButton)
closeButton.setFont(font)
closeButton.clicked.connect(window.close)

# Show the button
window.show()
