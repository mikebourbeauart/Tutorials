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
        self.button1 = QtGui.QPushButton()
        self.button1.setMaximumWidth(50)
        self.button2 = QtGui.QPushButton()
        self.button2.setMaximumWidth(50)
        self.button3 = QtGui.QPushButton()
        self.button3.setMaximumWidth(50)
        
    #-------------------------------------------
    def create_layout(self):
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        blank_layout = QtGui.QVBoxLayout()
        main_layout = QtGui.QHBoxLayout( self )
        main_layout.addLayout(blank_layout)
        main_layout.addLayout(layout)
        layout.addStretch()
        self.setLayout(layout)
        
    #-------------------------------------------
    def move_UI( self ):
        ''' Moves the UI to the cursor's position '''
        pos = QtGui.QCursor.pos()
        #self.move(pos.x()+20, pos.y()+15)
    
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
    def create_connections(self):
        # Left click
        self.button1.clicked.connect( self.on_left_click1 )
        self.button2.clicked.connect( self.on_left_click2 )
        self.button3.clicked.connect( self.on_left_click3 )
        
        # Right click delete
        delete = QtGui.QAction(self)
        delete.setText("remove")
        delete.triggered.connect(self.remove_button)
        self.addAction(delete)
        
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#
    def remove_button(self):
        self.deleteLater()
    
    def on_left_click1(self):
        self.popup = Popup_Window(self, self.button1 )                    # Passing button in so I can get it's position
        self.popup.show()
        
    def on_left_click2(self):
        self.popup = Popup_Window(self, self.button2 )      
        self.popup.show()
        
    def on_left_click3(self):
        self.popup = Popup_Window(self, self.button3 )      
        self.popup.show()
        
############################################
class Popup_Window( QtGui.QDialog ):
    def __init__( self, mainUIWindow, button ):
        super( Popup_Window, self ).__init__()
        
        self.button_pos = button                                           # Creating variable for the button
        self.mainUIWindow = mainUIWindow
        self.setAttribute( QtCore.Qt.WA_DeleteOnClose )
        #self.setMinimumWidth(100)                                         # I need a minimum width
        
        # Commands
        self.create_gui()
        self.create_layout()
        self.create_connections()
        self.move_UI()
        
    #-------------------------------------------
    def move_UI( self ):                                                    # Move popup based on pos of window and buttons
        ''' Moves the UI to the cursor's position '''
        self.setWindowFlags(QtCore.Qt.Popup)                               
        self.line_edit.setFocus()                             
        btn_global_point_y = self.button_pos.mapToGlobal(self.button_pos.rect().topLeft()).y()
        win_global_point_x = self.mapToGlobal(self.rect().topLeft()).x()
        win_global_point = self.mapToGlobal(self.rect().topLeft())
        self.move(win_global_point + QtCore.QPoint(self.width()+50, btn_global_point_y))                  # Here is where I find the distance between the window edge and button edge 
        
    #-------------------------------------------
    def create_gui( self ):
        ''' Visible GUI stuff '''
        self.my_label = QtGui.QLabel("default text")
        self.line_edit = QtGui.QLineEdit()
        self.line_edit.setMaxLength( 30 )
        self.push_btn = QtGui.QPushButton( "Hey" )
        self.push_btn.setMaximumWidth( 30 )
        
    #-------------------------------------------
    def create_layout( self ):
        self.button_layout = QtGui.QVBoxLayout()
        self.button_layout.addWidget( self.my_label )
        self.button_layout.addWidget( self.line_edit )
        self.button_layout.addWidget( self.push_btn )
        #self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.button_layout)
        
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
    def create_connections( self ):
        self.line_edit.textChanged.connect( self.on_text_changed )
        
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#
    def on_text_changed( self ):
        typed_name = self.line_edit.text()
        self.my_label.setText(typed_name)
        
        
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