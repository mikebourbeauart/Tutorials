from PySide import QtCore, QtGui
import maya.OpenMayaUI as mui
from shiboken import wrapInstance 

def get_parent():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance( long( ptr ), QtGui.QWidget )
    
############################################
class Tool_Window(QtGui.QDialog):
    def __init__(self, parent = get_parent() ):
        super(Tool_Window, self).__init__(parent)
                
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
        self.move(pos.x()+20, pos.y()+15)
    
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
        self.popup = Popup_Window( self, self.button1 )                    # Passing button in so I can get it's position
        self.popup.show()
        
    def on_left_click2(self):
        self.popup = Popup_Window( self, self.button2 )      
        self.popup.show()
        
    def on_left_click3(self):
        self.popup = Popup_Window( self, self.button3 )      
        self.popup.show()
        
############################################
class Popup_Window( QtGui.QDialog ):
    def __init__( self, toolWindow, button ):
        super( Popup_Window, self ).__init__()
        
        self.__popup_filter = ClosePopupFilter()
        self.installEventFilter(self.__popup_filter) 
        self.setWindowFlags(QtCore.Qt.Popup)
        '''
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.CustomizeWindowHint |
                            QtCore.Qt.Tool)    
        '''
        self.button_pos = button       
        self.toolWindow = toolWindow                                        
        self.setAttribute( QtCore.Qt.WA_DeleteOnClose )
        self.resize(100, 100) 
        
        # Commands
        self.create_gui()
        self.create_layout()
        self.create_connections()
        self.move_UI()        
        
    #-------------------------------------------
    def move_UI( self ):                                                        # Method that I use to place the popup window initially  
        self.line_edit.setFocus() 
        # Get button position                                          
        self.btn_global_point = self.button_pos.mapToGlobal(self.button_pos.rect().topLeft())  
        print self.btn_global_point
        # Get window position  
        self.win_global_point = self.toolWindow.mapToGlobal(self.rect().topLeft()) 
        print self.win_global_point
        # Get popup Size
        self.popup_size = self.mapToGlobal(self.rect().topRight())
        print self.popup_size
        # Move the window
        self.move((self.win_global_point.x()-self.popup_size.x()), self.btn_global_point.y())
        
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
        #self.move_UI() 
        typed_name = self.line_edit.text()
        self.my_label.setText(typed_name) 
                                                                 # I reuse the move method to move the ui on text edit

############################################
class  ClosePopupFilter(QtCore.QObject):
    ''' Close popup window '''
    def  eventFilter(self, target, event):
        if event.type() == QtCore.QEvent.WindowDeactivate:
            target.close()
        return  False
        
        
        
if __name__ == '__main__':
    # Things to fix PySide Maya bug
    try:
        test_ui.close()
        test_ui.deleteLater()
    except:
        pass
        
    test_ui = Tool_Window()
    test_ui.show()

    try:
        test_ui.show()
    except:
        test_ui.close()
        test_ui.deleteLater()