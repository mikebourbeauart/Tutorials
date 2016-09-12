
def get_parent():
	try:
		from shiboken import wrapInstance
		import maya.OpenMayaUI as mui

		ptr = mui.MQtUtil.mainWindow()
		return wrapInstance( long( ptr ), QtGui.QWidget )
	except:
		return None

############################################
if __name__ == "__main__":
	# workaround for a bug in maya
	try:
		tree_view_ui.close()
		tree_view_ui.deleteLater()
	except:
		pass
		
	tree_view_ui = Main_Window()
	tree_view_ui.show()

	try:
		tree_view_ui.show()
	except:
		tree_view_ui.close()
		tree_view_ui.deleteLater()
		