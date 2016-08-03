from PySide import QtCore, QtGui
from shiboken import wrapInstance 

def get_parent():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance( long( ptr ), QtGui.QWidget )
    
############################################
class RightClickMenuButton(QtGui.QDialog):
    def __init__(self, parent = get_parent() ):
        super(RightClickMenuButton, self).__init__(parent)
        
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        
        # Commands
        self.move_UI()
        self.create_gui()
        self.create_layout()
        self.create_connections()
        
    #-------------------------------------------
    def create_gui(self):
        self.button = QtGui.QPushButton()
        
    #-------------------------------------------
    def create_layout(self):
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)
        
    #-------------------------------------------
    def move_UI( self ):
        ''' Moves the UI to the cursor's position '''
        pos = QtGui.QCursor.pos()
        self.move(pos.x()+20, pos.y()+15)
    
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
    def create_connections(self):
        # Left click
        self.button.clicked.connect( self.on_left_click )
        
        # Right click delete
        delete = QtGui.QAction(self)
        delete.setText("remove")
        delete.triggered.connect(self.remove_button)
        self.addAction(delete)
        
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#-
    def remove_button(self):
        self.deleteLater()
    
    def on_left_click(self):
        self.popup = Popup_Window(self, self.button )      # Passing button in so I can get it's position
        self.popup.show()
        
############################################
class Popup_Window( QtGui.QDialog ):
    def __init__( self, mainUIWindow, button ):
        super( Popup_Window, self ).__init__()
        
        self.button_pos = button                           # Creating variable 
        self.mainUIWindow = mainUIWindow
        self.setAttribute( QtCore.Qt.WA_DeleteOnClose )
        
        # Commands
        self.move_UI()
        self.create_gui()
        self.create_layout()
        
    #-------------------------------------------
    def move_UI( self ):
        ''' Moves the UI to the cursor's position '''
        rel_pos = self.button_pos.pos()
        pos = self.button_pos.mapToGlobal(rel_pos)
        self.move(pos.x()+20, pos.y()+15)
        
    #-------------------------------------------
    def create_gui( self ):
        ''' Visible GUI stuff '''
        self.push_btn = QtGui.QPushButton( "Create" )
        
    #-------------------------------------------
    def create_layout( self ):
        self.label = QtGui.QLabel( "Hey" )
        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addWidget( self.push_btn )
        
        
if __name__ == '__main__':
    # Things to fix PySide Maya bug
    try:
        test_ui.close()
        test_ui.deleteLater()
    except:
        pass
        
    test_ui = RightClickMenuButton()
    test_ui.show()

    try:
        test_ui.show()
    except:
        test_ui.close()
        test_ui.deleteLater()