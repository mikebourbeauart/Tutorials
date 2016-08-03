import sys, os
from PySide import QtCore, QtGui
from shiboken import wrapInstance
import maya.OpenMayaUI as mui

def get_parent():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance( long( ptr ), QtGui.QWidget )   
 
class Main_Window(QtGui.QDialog):
     
    def __init__(self, parent = get_parent()):
        super(Main_Window, self).__init__(parent)
        
        # Commands
        self.create_gui()
        self.create_layout()
        self.create_actions()
        #self.create_connections()
        #self.get_contents()
        
    def create_gui( self ):
        self.tw_file_list = Tree_View( self )
        # How to resize based on size of item
        #self.tw_file_list.header().setResizeMode( 0, QtGui.QHeaderView.ResizeToContents )
        # How to change cursor on mouse over
        #self.header().viewport().setCursor(QtCore.Qt.PointingHandCursor)
        self.tw_file_list.setHeaderLabels(["Current Directory", "Comments"])
        self.name = "a"
        self.date = "b"
        self.parent = self.tw_file_list.invisibleRootItem()
        self.add_item( self.name, self.date, self.parent)
        self.add_item("top", "12/30/2014", self.tw_file_list.invisibleRootItem())
        self.item = self.add_item("item", "12/29/2014", self.tw_file_list.invisibleRootItem())
        self.add_item("subitem", "12/28/2014", self.item)
        
    def create_layout( self ):
        self.layout = QtGui.QHBoxLayout( self )
        self.layout.addWidget(self.tw_file_list)
        self.setLayout( self.layout )

    def add_item(self, name, date, parent):
        item = QtGui.QTreeWidgetItem(parent)
        item.setText(0, name)
        item.setText(1, date)
        #It is important to set the Flag Qt.ItemIsEditable
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEditable)
        item.setIcon(0,QtGui.QIcon(":/menuIconFile.png"))
        return item

    def get_contents( self, path ):
        self.tw_file_list.clear()
        path = "S:/abc_testproject_12345/Sequences/ANA30secService/Sh010/Modeling/Production/Maya/scenes/bus"
        contents = os.listdir( path )
        
        contents = [("file_01","1/1/2015"), ("file_02","1/2/2015"), ("file_03","1/3/2015")]

        for self.item, self.date in contents:
            self.add_item( self.item, self.date, self.tw_file_list.invisibleRootItem() )
               

    def create_actions( self ):
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.actionEdit = QtGui.QAction("New Folder", self)
        self.addAction(self.actionEdit)
        self.actionDelete = QtGui.QAction("Delete", self)
        self.addAction(self.actionDelete)
        self.style()
    '''
    # Connections
    def create_connections( self ):
        self.actionEdit.triggered.connect(self.add_item_action)
        self.actionDelete.triggered.connect(self.delete_item)
        
    # Slots #############################################################
    def add_item_action(self):
        parent = self.tw_file_list.currentItem()
        self.tw_file_list.expandItem(parent)
        if parent is None:
            parent = self.tw_file_list.invisibleRootItem()
        new_item = self.add_item("New Folder", "date", parent)
        self.editItem(new_item)
     
    def delete_item(self):
        root = self.tw_file_list.invisibleRootItem()
        for item in self.tw_file_list.selectedItems():
            (item.parent() or root).removeChild(item)
    '''
############################################
class Tree_View( QtGui.QTreeView ):
    ''' Create the file filters '''
    def __init__( self, model, parent=get_parent() ):
        super( Tree_View, self ).__init__( parent )
        

        
        # Setup UI

        self.setColumnWidth(0, 370)
        #self.setColumnWidth(1,200)
        self.header().setResizeMode( 1, QtGui.QHeaderView.ResizeToContents )
        self.header().setStretchLastSection(True)
        self.header().setResizeMode(1, QtGui.QHeaderView.Stretch)
        #self.header().viewport().setCursor(QtCore.Qt.PointingHandCursor)
        self.parent = self.invisibleRootItem()

############################################
if __name__ == "__main__":
    # Development stuff
    try:
        treeWidget_ui.close()
        treeWidget_ui.deleteLater()
    except:
        pass
    
    # Show stuff
    treeWidget_ui = Main_Window()
    treeWidget_ui.show()

    # Development stuff
    try:
        treeWidget_ui.show()
    except:
        treeWidget_ui.close()
        treeWidget_ui.deleteLater()
    

     
