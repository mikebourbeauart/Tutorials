import sys

from PySide import QtGui
from PySide import QtCore

class Build(QtGui.QDialog):

	'''Main functions to build AAM UI'''

	def __init__(self):
		super(Build, self).__init__()

		self.create_gui()
		self.create_layout()
		#self.create_connections()

	#-----------------------------------------------------------------
	def create_gui(self):
		'''Main window GUI stuff'''

		# Header widgets
		self.le_address_bar = QtGui.QLineEdit()
		self.le_address_bar.setText('hello')
		self.le_address_bar.setReadOnly(True)

		self.btn_browse_folders = QtGui.QPushButton('browse')
		self.btn_browse_folders.setMaximumHeight( 50 )

		# Initially hidden widgets
		self.tv_browse_folders = QtGui.QTreeView(self)

		# Cover widgets
		self.main_tab_widget = QtGui.QTabWidget()		
		self.tabw_manager = QtGui.QWidget()
		self.tabw_import = QtGui.QWidget()
		self.tabw_publish = QtGui.QWidget()

		self.main_tab_widget.addTab( self.tabw_manager, "Manager" )
		self.main_tab_widget.addTab( self.tabw_import, "Import" )
		self.main_tab_widget.addTab( self.tabw_publish, "Publish" )
		self.main_tab_widget.setCurrentIndex(1)	

		# State machine
		self.machine = QtCore.QStateMachine()
		state1 = QtCore.QState(self.machine)
		state2 = QtCore.QState(self.machine)
		self.machine.setInitialState(state1)                                               # Looks like state isn't being set

		# States
		state1.assignProperty(self.main_tab_widget, 'pos', QtCore.QPointF(11, 40))
		state1.assignProperty(self.tv_browse_folders, 'pos', QtCore.QPointF(11, -200))
		state2.assignProperty(self.main_tab_widget, 'pos', QtCore.QPointF(11, 240))
		state2.assignProperty(self.tv_browse_folders, 'pos', QtCore.QPointF(11, 40))

		# Transitions
		t1 = state1.addTransition(self.btn_browse_folders.clicked, state2)
		t1.addAnimation(QtCore.QPropertyAnimation(self.main_tab_widget, 'pos', state1))
		t1.addAnimation(QtCore.QPropertyAnimation(self.tv_browse_folders, 'pos', state1))

		t2 = state2.addTransition(self.btn_browse_folders.clicked, state1)
		t2.addAnimation(QtCore.QPropertyAnimation(self.main_tab_widget, 'pos', state2))
		t2.addAnimation(QtCore.QPropertyAnimation(self.tv_browse_folders, 'pos', state2))

		self.machine.start()

	#-----------------------------------------------------------------
	def create_layout( self ):
		'''Create main window layout'''
		
		address_bar_layout = QtGui.QBoxLayout( QtGui.QBoxLayout.LeftToRight)
		address_bar_layout.addWidget( self.le_address_bar )
		address_bar_layout.addWidget( self.btn_browse_folders )
		
		self.main_layout = QtGui.QVBoxLayout()
		self.main_layout.addLayout( address_bar_layout )
		self.main_layout.addWidget( self.tv_browse_folders )
		self.main_layout.addWidget( self.main_tab_widget )

		self.setLayout( self.main_layout )

	#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
	#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
	#def create_connections(self):
	#	self.btn_browse_folders.clicked.connect(self.run_state_machine)

	##-----#-----#-----#-----#-----#-----#-----#-----#-----#
	#def run_state_machine(self):

		

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	entity_browser_ui = Build()
	entity_browser_ui.show()
	sys.exit(app.exec_())