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
        # Create the selected item list
        self.selection_list = QtGui.QListWidget()
        
        # Create Refresh and Cancel buttons
        self.refresh_button = QtGui.QPushButton("Refresh")
        self.cancel_button = QtGui.QPushButton("Cancel")        

        # Create the button layout
        button_layout = QtGui.QHBoxLayout()
        button_layout.setSpacing(2)
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.cancel_button)        
        
        # Create the main layout
        main_layout = QtGui.QVBoxLayout()
        main_layout.setSpacing(2)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.addWidget(self.selection_list)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
    def create_connections(self):
        
        # Connect the selected item list widget
        self.connect(self.selection_list, 
                     QtCore.SIGNAL("currentItemChanged(QListWidgetItem*, QListWidgetItem*)"), 
                     self.set_current_item)
        self.connect(self.selection_list, 
                     QtCore.SIGNAL("itemChanged(QListWidgetItem*)"), 
                     self.update_name)
        
        # Connect the buttons
        self.connect(self.refresh_button, QtCore.SIGNAL("clicked()"), self.refresh)
        self.connect(self.cancel_button, QtCore.SIGNAL("clicked()"), self.close_dialog)
        
    def update_selection(self):
        # Remove all items from the list before repopulating
        self.selection_list.clear()
        
        # Add the currently selected objects to the list
        selected = mc.ls(selection=True)
        for sel in selected:
            item = QtGui.QListWidgetItem(sel)
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
        self.current_item_name = str(mc.rename(self.current_item_name, new_name))
        item.setText(self.current_item_name)
            

        
if __name__ == "__main__":
    dialog = RenamingDialog()
    
    dialog.show()