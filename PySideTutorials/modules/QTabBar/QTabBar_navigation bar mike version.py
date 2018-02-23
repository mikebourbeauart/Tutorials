import os
import sys

from PySide import QtGui
from PySide import QtCore

shared_path = os.path.abspath(
		os.path.join(os.path.dirname(__file__), '..')
	)

if not shared_path in sys.path:
	sys.path.append(shared_path)

from __shared import window_utils


class MainWindow( QtGui.QDialog ):
	def __init__( self, parent=window_utils.get_ui_parent() ):
		super( MainWindow, self ).__init__( parent )




		self.create_gui()
		self.create_layout()
		#self.create_connections()
		self.get_contents()
		
	#--------------------------------------------------------------------
	def create_gui( self ):

		self.navigation_bar = NavigationBar()
		self.navigation_bar.setExpanding(False)
		self.navigation_bar.setDrawBase(False)

		self.proxy = QtGui.QSortFilterProxyModel(self)
		self.model = MyModel()

	#--------------------------------------------------------------------
	def create_layout( self ):

		self.headerLayout = QtGui.QHBoxLayout()
		self.headerLayout.addWidget(self.navigation_bar, stretch=1)

		main_layout = QtGui.QVBoxLayout( self )
		main_layout.addWidget( self.navigation_bar )
		#self.main_layout.addWidget( self.tv_file_list )
		self.setLayout(main_layout)
		
	#--------------------------------------------------------------------
	def get_contents(self):
		self.model.clear()
		contents=["path1","path2"]
		for path in contents:
			self.add_file(path)
			
	#--------------------------------------------------------------------
	def add_file(self, name):
		self.navigation_bar.addTab(name)
		
	def _updateNavigationBar(self):
		'''Update navigation bar.'''
		if self._updatingNavigationBar:
			return

		self._updatingNavigationBar = True

		# Clear all existing entries.
		for index in range(self.navigationBar.count(), -1, -1):
			self.navigationBar.removeTab(index)

		# Compute new entries.
		entries = []
		index = self.view.rootIndex()
		while index.isValid():
			item = self.model.item(index)
			entries.append(
				dict(icon=item.icon, label=item.name, index=index)
			)
			index = self.model.parent(index)

		item = self.model.root
		entries.append(
			dict(icon=item.icon, label=item.name, index=None)
		)

		entries.reverse()
		for entry in entries:
			tabIndex = self.navigationBar.addTab(entry['icon'], entry['label'])
			self.navigationBar.setTabData(tabIndex, entry['index'])
			self.navigationBar.setCurrentIndex(tabIndex)

		self._updatingNavigationBar = False

	def _onSelectNavigationBarItem(self, index):
		'''Handle selection of navigation bar item.'''
		if index < 0:
			return

		if self._updatingNavigationBar:
			return

		modelIndex = self.navigationBar.tabData(index)
		self.setLocationFromIndex(modelIndex)
		
	##--------------------------------------------------------------------
	#def handleItemEntered(self, index):
	#	if index.isValid():
	#		QtGui.QToolTip.showText(
	#			QtGui.QCursor.pos(),
	#			index.data(),
	#			self.tv_file_list.viewport(),
	#			self.tv_file_list.visualRect(index)
	#			)

	##--------------------------------------------------------------------
	#def create_connections( self ):
	#	self.tv_file_list.clicked.connect( self.on_click )
	#	self.tv_file_list.entered.connect( self.handleItemEntered )
		
	## slots --------------------------------------------------------------
	#def on_click(self, item ):
	#	index = self.tv_file_list.selectedIndexes()[0]
	#	item = self.tv_model.itemFromIndex(index).text()
	#	print item


############################################
class MyModel(QtGui.QStandardItemModel):
	def __init__(self, parent=None):
		super(MyModel, self).__init__(parent)
		
	def flags(self, index):
		flag = QtCore.Qt.ItemIsEnabled
		if index.isValid():
			flag |= QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable 
		return flag
		


class NavigationBar(QtGui.QTabBar):
	'''Entity browser.'''


	def __init__(self):
		'''Initialise browser with *root* entity.

		Use an empty *root* to start with list of projects.

		*parent* is the optional owner of this UI element.

		'''
		super(NavigationBar, self).__init__()

		self._create_gui()

	def _create_gui(self):
		'''Construct widget.'''

		self.setExpanding(False)
		self.setDrawBase(False)


		

app = QtGui.QApplication(sys.argv)
entity_browser_ui = MainWindow()
entity_browser_ui.show()
sys.exit(app.exec_())

		
  





