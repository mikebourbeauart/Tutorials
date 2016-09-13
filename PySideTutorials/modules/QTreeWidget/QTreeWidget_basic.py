import sys, os, time
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
        self.get_contents( None )
        
    def create_gui( self ):
        self.tw_file_list = File_List( self )
        self.parent = self.tw_file_list.invisibleRootItem()
        
    def create_layout( self ):
        self.layout = QtGui.QHBoxLayout( self )
        self.layout.addWidget(self.tw_file_list)
        self.setLayout( self.layout )

    def get_contents( self, path ):
        self.tw_file_list.clear()
        path = "C:\Program Files"
        contents = os.listdir( path )

        for item in contents:
            print item
            parent = self.tw_file_list.invisibleRootItem()
            date = self.get_date( item, path)
            self.add_item(item, date, parent)
            
    def add_item(self, name, date, parent):
        item = QtGui.QTreeWidgetItem(parent)
        item.setText(0, name)
        item.setText(1, date)
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled )
        return item
    
    def get_date( self, item, path):
        path = "C:\Program Files"
        file = str(path + "/" + item)
        date = time.localtime(os.path.getmtime(file))
        clean_date = "{0}_{1}_{2}  {3}:{4}".format( date[0], date[1], date[2], date[3], str(date[4]).zfill(2) )
        return clean_date    
    
############################################
class File_List( QtGui.QTreeWidget ):
    ''' Create the file filters '''
    def __init__( self, parent=get_parent() ):
        super( File_List, self ).__init__( parent )
        
        # Setup UI
        self.setColumnCount(2)
        self.setHeaderLabels(["name","date"])
        self.parent = self.invisibleRootItem()

############################################
if __name__ == "__main__":
    # Workaround hack for a PySide bug within maya
    try:
        main_ui.close()
        main_ui.deleteLater()
    except:
        pass
    
    # Show stuff
    main_ui = Main_Window()
    main_ui.show()

    try:
        main_ui.show()
    except:
        main_ui.close()
        main_ui.deleteLater()
    

     
