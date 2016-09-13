from PySide import QtGui


def get_ui_parent():
	try:
		from shiboken import wrapInstance
		import maya.OpenMayaUI as mui

		ptr = mui.MQtUtil.mainWindow()
		return wrapInstance( long( ptr ), QtGui.QWidget )
	except:
		return None