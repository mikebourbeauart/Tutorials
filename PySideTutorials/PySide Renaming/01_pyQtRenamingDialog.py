from PySide import QtCore, QtGui
from shiboken import wrapInstance 
import maya.cmds as mc
import maya.OpenMayaUI as mui


def maya_main_window():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance( long( ptr ), QtGui.QWidget )
    
# UI class
class RenamingDialog( QtGui.QDialog ):
    
    def __init__( self, parent=maya_main_window() ):
        super( RenamingDialog, self ).__init__( parent )
        
        self.setWindowTitle("Renaming Dialog")
        self.setFixedSize(250, 200)
        
        self.create_layout()
        self.create_connections()
        
        self.refresh()
        
    def create_layout(self):
        
        self.selection_list = QtGui.QListWidget()
        
        self.refresh_button = QtGui.QPushButton("Refresh")
        self.cancel_button= QtGui.QPushButton("Cancel")
        self.setAttribute( QtCore.Qt.WA_DeleteOnClose )
        button_layout = QtGui.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.cancel_button)
        
        main_layout = QtGui.QVBoxLayout()
        main_layout.setSpacing(2)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.addWidget(self.selection_list)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
    def create_connections(self):
        
        self.connect(self.selection_list, 
                     QtCore.SIGNAL("currentItemChanged(QListWidgetItem*, QListWidgetItem*)"),
                     self.set_current_item)
        self.connect(self.selection_list, 
                     QtCore.SIGNAL("itemChanged(QListWidgetItem*)"),
                     self.update_name)
        
        self.connect(self.refresh_button, QtCore.SIGNAL("clicked()"), self.refresh)
        self.connect(self.cancel_button, QtCore.SIGNAL("clicked()"), self.close_dialog)
        
    def update_selection(self):
        self.selection_list.clear()
        
        selected = mc.ls( sl=1 )
        for i in selected:
            item = QtGui.QListWidgetItem(i)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            self.selection_list.addItem(item)
        
        
    #--------------------------------------------------------------------------
    # SLOTS
    #--------------------------------------------------------------------------  
    def refresh(self):
        self.update_selection()
        
    def close_dialog(self):
        self.close()
        
    def set_current_item(self, item):
        if (item):
            self.current_item_name = str(item.text())
        else:
            self.current_item_name = ""
            
    def update_name(self, item):
        new_name = str(item.text())
        
        # Ignore if the name hasn't change
        if new_name == self.current_item_name:
            return
            
        # Restore the previous name if a new name isn't given
        if not new_name:
            item.setText(self.current_item_name)
            return
            
        # Update the name in Maya
        # Maya may alter the name so update the list accordingly
        self.current_item_name = str(mc.renam(self.current_item_name, new_name))
        item.setText(self.current_item_name)
        
        

if __name__ == "__main__":
    dialog = RenamingDialog()
    
    dialog.show()

'''
if __name__ == "__main__":

    # Development workaround for PySide error (Maya 2014)
    # Make sure the UI is deleted before recreating
    try:
        renamingDialog_ui.close()
        renamingDialog_ui.deleteLater()
    except:
        pass

    # Create minimal UI object
    renamingDialog_ui = RenamingDialog()
    
    # Delete the UI if errors occur to avoid causing 
    # and event errors (in Maya 2014)
    try:
        renamingDialog_ui.create_layout()
        renamingDialog_ui.show()
    except:
        renamingDialog_ui.close()
        renamingDialog_ui.deleteLater()
        traceback.print_exc()    
'''
    