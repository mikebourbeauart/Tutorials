import traceback
from PySide import QtCore, QtGui
from shiboken import wrapInstance
import maya.cmds as cmds
import maya.OpenMayaUI as omui
import pymel.core as pm

# Some random class
class MyCustomType(object):
    
    def __init__(self, aName, anObject):
        self.name = aName
        self.object = anObject

def maya_main_window():
    '''
    Return the Maya main window widget as a Python object
    '''
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtGui.QWidget)
   

class TestUi(QtGui.QDialog):
       
    def __init__(self, parent=maya_main_window()):
        super(TestUi, self).__init__(parent)
           
        
    def create(self):
        '''
        Set up the UI prior to display
        '''
        self.setWindowTitle("Hello Tree Widget!")
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setup_widget()
        
    def setup_widget(self):
        '''
        Create the widgets for the dialog
        '''        
        
        
        item_dict = {"A":[1,2,3], "B":[4,5,6], "C":[7,8,9]}
        
        
        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.setColumnCount(3)
        # use an event filter to prevent the event bubbeling up
        # to avoid mayas pickwalk to kick in
        self.treeWidget.installEventFilter(self)
        
        
        for key in sorted(item_dict):
            #print item_dict.get(key)
            
            parent = QtGui.QTreeWidgetItem(self.treeWidget)
            parent.setText(0, key)
            parent.setText(1, 'Multimatte')
            
            for child in item_dict.get(key):
                
                i = QtGui.QTreeWidgetItem(parent)
                i.setText(0, 'Child:{0}'.format(child))
                i.setText(1, 'Second Col:{0}'.format(child))
                i.setText(2, 'Third Col:{0}'.format(child))
                
                # Create a custom data type and a tree item
                myObject = MyCustomType('Name:{0}'.format(child), 'Object:{0}'.format(child))
                
                # Set our instance as a custom data role
                # On top of the standard roles that Qt uses such as DisplayRole, TextAlignmentRole, ...
                # We can add our own data from anything starting with UserRole and higher
                # Qt wont touch roles this high up
                i.setData(0, QtCore.Qt.UserRole + 1, myObject)
                i.setData(1, QtCore.Qt.DisplayRole, 'A string')
            
            
        main_layout = QtGui.QVBoxLayout()
        main_layout.setContentsMargins(6, 6, 6, 6)

        main_layout.addWidget(self.treeWidget)
    
        self.setLayout(main_layout)
        
        self.treeWidget.currentItemChanged.connect(self.on_selection_changed)
        self.treeWidget.itemClicked.connect(self.on_clicked) 
        
        
    def eventFilter(self, obj, event):
        # watch for keypress on the treeWidget and
        # handle the directly. Make sure Maya doesn´t
        # also get them and run operations on thter
        # of the interface. Accepting the event prevents
        # them from bubbeling up to parent widgets.
        # this will prevent mayas pickwalking behaviour
        # when using the arrow keys.
        if obj is self.treeWidget:
            if event.type() == event.KeyPress:
                self.treeWidget.keyPressEvent(event)
                event.accept()
                # Don´t pass this event on to the actual widget
                # it is filtered.
                return True
        
        # returning False for anything else means to just let
        # the original widget handle this event
        return False
                
    #--------------------------------------------------------------------------
    # SLOTS
    #--------------------------------------------------------------------------
        
    def on_selection_changed(self, current, previous):
        
        if current.parent() is not None:
            
            print('Text: {0}'.format(current.text(0)))
            data = current.data(0, QtCore.Qt.UserRole + 1)
            print('Data Name: {0}'.format(data.name))
            print('Data Object: {0}'.format(data.object))
         
        else:
            print('Text: {0}'.format(current.text(0)))
            
    def on_clicked(self, item, column):
        
        if item.parent() is not None:
            
            # Now fetch it back out again by row, column
            #item = self.treeWidget.itemAt(0, 0)
            data_0 = item.data(0, QtCore.Qt.UserRole + 1)
            data_1 = item.data(1, QtCore.Qt.DisplayRole)
            
            print('\n---------------')
            print('Custom Data Name: {0}'.format(data_0.name))
            print('Custom Data Object: {0}'.format(data_0.object))
            print('Data: {0}'.format(data_1))
            print('---------------')

        else:
            print('{0} has {1} child items'.format(item.text(0), item.childCount()))

              
if __name__ == "__main__":
    
    # Development workaround for PySide winEvent error (in Maya 2014)
    # Make sure the UI is deleted before recreating
    try:
        test_ui.deleteLater()
    except:
        pass
    
    # Create minimal UI object
    test_ui = TestUi()
    
    # Delete the UI if errors occur to avoid causing winEvent
    # and event errors (in Maya 2014)
    try:
        test_ui.create()
        test_ui.show()
    except:
        test_ui.deleteLater()
        traceback.print_exc()