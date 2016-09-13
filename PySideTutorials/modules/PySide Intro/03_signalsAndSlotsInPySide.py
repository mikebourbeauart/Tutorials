import traceback

from PySide import QtCore 
from PySide import QtGui 

from shiboken import wrapInstance 

import maya.cmds as mc
import maya.OpenMayaUI as omui

# Signals and slots are a construct in Qt that allow objects to communicate with one another
    # For a example when a button is clicked a signal is emitted and any recieving objects that have a connection to that signal will call that corresponding slot and execute that code within it
    # In PySide slots are no different than other methods inside your class
    # All that is required to allow 2 objects to communitcate is to create a connection between a signal and a slot
    
# Maya main window function
def maya_main_window():
    '''
    Return the Maya main window widget as a Python object
    '''
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtGui.QWidget)
    

# Test Ui class which is extending the QDialog
class TestUi(QtGui.QDialog):
    
    test_signal = QtCore.Signal()
    
    # Basic init method that just calls the parent class
    def __init__(self, parent=maya_main_window()):
        super(TestUi, self).__init__(parent)
        
    # 4 methods for creating the dialog:
    # Main create method, create_controls, create_layout, and create_connections
    def create(self):
        '''
        Create the UI
        '''
        self.setWindowTitle("TestUi")
        self.setWindowFlags(QtCore.Qt.Tool)
        
        self.create_controls()
        self.create_layout()
        self.create_connections()
    
    # Create controls and create layout create the visible dialog
    def create_controls(self):
        '''
        Create the widgets for the dialog
        '''
        self.push_button = QtGui.QPushButton("QPushButton")
        self.check_box_01 = QtGui.QCheckBox("QCheckBox 01")
        self.check_box_02 = QtGui.QCheckBox("QCheckBox 02")
        
        self.line_edit = QtGui.QLineEdit("QLineEdit")
        self.list_wdg = QtGui.QListWidget()
        self.list_wdg.addItems(["QListWidgetItem 01", 
                                "QListWidgetItem 02", 
                                "QListWidgetItem 03", 
                                "QListWidgetItem 04"])
        self.list_wdg.setCurrentRow(0)
        self.list_wdg.setMaximumHeight(60)
        
    def create_layout(self):
        '''
        Create the layouts and add widgets
        '''
        check_box_layout = QtGui.QHBoxLayout()
        check_box_layout.setContentsMargins(2, 2, 2, 2)
        check_box_layout.addWidget(self.check_box_01)
        check_box_layout.addWidget(self.check_box_02)
        
        
        main_layout = QtGui.QVBoxLayout()
        main_layout.setContentsMargins(6, 6, 6, 6)
        
        main_layout.addWidget(self.push_button)
        main_layout.addLayout(check_box_layout)
        main_layout.addWidget(self.line_edit)
        main_layout.addWidget(self.list_wdg)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
    
    # This is where we add the connections that allow our controls to send signals and that will be received by our test_Ui class
    def create_connections(self):
        '''
        Create the signal/slot connections
        '''
        self.push_button.clicked.connect( self.on_button_pressed )
        self.check_box_01.toggled.connect( self.on_check_box_toggled )
        self.check_box_02.toggled.connect( self.on_check_box_toggled )
        
        #self.line_edit.textChanged.connect(self.on_text_changed)
        self.line_edit.editingFinished.connect( self.on_text_changed )
        
        self.list_wdg.currentItemChanged.connect( self.on_selection_changed )
        
        self.test_signal.connect( self.on_test_signal_emitted )
        
    #--------------------------------------------------------------------------
    # SLOTS
    #--------------------------------------------------------------------------
    # These are the methods that will be called when the diff signals from our controls are emitted
    def on_button_pressed(self):
        print("Button pressed")
        
        if self.line_edit.text() == "emit":
            self.test_signal.emit()
        
    def on_check_box_toggled(self):
        #print("Checkbox toggled")
        sender = self.sender()
        print( "{0} toggled".format(sender.text()) )
        
    def on_text_changed(self):
        print("Text changed")
        
    def on_selection_changed(self, current, previous):
        print("Selection changed")
        print( "Current Item: {0}".format(current.text()) )
        print( "Previous Item: {0}".format(previous.text()) )
    def on_test_signal_emitted(self):
        print("Signal received")          
          
               
if __name__ == "__main__":

    # Development workaround for PySide error (Maya 2014)
    # Make sure the UI is deleted before recreating
    try:
        test_ui.close()
        test_ui.deleteLater()
    except:
        pass

    # Create minimal UI object
    test_ui = TestUi()
    
    # Delete the UI if errors occur to avoid causing 
    # and event errors (in Maya 2014)
    try:
        test_ui.create()
        test_ui.show()
    except:
        test_ui.close()
        test_ui.deleteLater()
        traceback.print_exc()    