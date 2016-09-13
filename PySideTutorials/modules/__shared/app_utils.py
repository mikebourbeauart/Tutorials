import sys

from PySide import QtGui


def run_app(
	wMainWindowClass = None,
	isMaya = False
):
	'''Run *wMainWindowClass if *isMaya* is True or False'''

	window_class = wMainWindowClass()

	if __name__ == "__main__":

		if isMaya == True:

			# workaround for a bug in maya
			try:
				tree_view_ui.close()
				tree_view_ui.deleteLater()
			except:
				pass
		
			window_class = wMainWindowClass()
			tree_view_ui.show()

			try:
				tree_view_ui.show()
			except:
				tree_view_ui.close()
				tree_view_ui.deleteLater()
		else:
			app = QtGui.QApplication(sys.argv)
			entity_browser_ui = window_class
			entity_browser_ui.show()
			sys.exit(app.exec_())