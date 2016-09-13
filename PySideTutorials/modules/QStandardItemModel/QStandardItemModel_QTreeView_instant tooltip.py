from PySide import QtCore, QtGui

# Get __shared imported and working
import os
import sys

shared_path = os.path.abspath(
		os.path.join(os.path.dirname(__file__), '..')
	)

if not shared_path in sys.path:
	sys.path.append(shared_path)

from __shared import app_utils
from __shared import window_utils

############################################        
''' Classes '''
############################################
class Main_Window( QtGui.QDialog ):
	def __init__( self, parent=window_utils.get_ui_parent() ):
		super( Main_Window, self ).__init__( parent )
		print 'hey'
		self.create_gui()
		self.create_layout()
		self.create_connections()
		self.get_contents()
		
	#--------------------------------------------------------------------
	def create_gui( self ):
		self.tv_model=MyModel()
		self.tv_file_list = File_List( self )
		self.tv_file_list.setMouseTracking(True)
		
	#--------------------------------------------------------------------
	def create_layout( self ):
		self.main_layout = QtGui.QVBoxLayout( self )
		self.main_layout.addWidget( self.tv_file_list )
		self.setLayout( self.main_layout )
		
	#--------------------------------------------------------------------
	def get_contents(self):
		self.tv_model.clear()
		self.tv_model.setHorizontalHeaderLabels(["name","date"])
		contents=["path1","path2"]
		for path in contents:
			date = self.get_date(path)
			self.add_file(path,date)
		self.tv_file_list.setColumnWidth(0, 150)
			
	#--------------------------------------------------------------------
	def add_file(self, name, date):
		name = QtGui.QStandardItem(name)
		user = "me"
		name.setToolTip("<b>{0}</b><br><b>{1}</b>".format(name.text(), user) )                                            # Here's where I set the tooltip
		name.setIcon(self.style().standardIcon(QtGui.QStyle.SP_DirOpenIcon))
		date = QtGui.QStandardItem(date)
		self.tv_model.appendRow([name, date])
		
		
	#--------------------------------------------------------------------
	def get_date(self, path):
		return "a date"
		
	#--------------------------------------------------------------------
	def handleItemEntered(self, index):
		if index.isValid():
			QtGui.QToolTip.showText(
				QtGui.QCursor.pos(),
				index.data(),
				self.tv_file_list.viewport(),
				self.tv_file_list.visualRect(index)
				)

	#--------------------------------------------------------------------
	def create_connections( self ):
		self.tv_file_list.clicked.connect( self.on_click )
		self.tv_file_list.entered.connect( self.handleItemEntered )
		
	# slots --------------------------------------------------------------
	def on_click(self, item ):
		index = self.tv_file_list.selectedIndexes()[0]
		item = self.tv_model.itemFromIndex(index).text()
		print item


############################################
class MyModel(QtGui.QStandardItemModel):
	def __init__(self, parent=None):
		super(MyModel, self).__init__(parent)
		
	def flags(self, index):
		flag = QtCore.Qt.ItemIsEnabled
		if index.isValid():
			flag |= QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable 
		return flag
		
############################################
class File_List( QtGui.QTreeView ):
	''' Create the file filters '''
	def __init__( self, parent=None ):
		super( File_List, self ).__init__( parent )
		
		self.setModel(parent.tv_model)
		self.setIndentation(0)
		self.setColumnWidth(0,500)
		self.setFocusPolicy(QtCore.Qt.NoFocus)
		self.setStyleSheet("QToolTip { color: rgb(170,170,170); background-color: rgb(20,20,20); border: 1px rgb(20,20,20); }")


app = QtGui.QApplication(sys.argv)
entity_browser_ui = Main_Window()
entity_browser_ui.show()
sys.exit(app.exec_())

