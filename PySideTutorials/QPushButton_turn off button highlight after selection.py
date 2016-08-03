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
        self.create_gui()
        self.create_layout()
        self.create_connections()

    #-------------------------------------------
    def create_gui(self):
        self.button1 = Push_Buttons()
        self.button1.setMaximumWidth(50)
        self.button2 = Push_Buttons()
        self.button2.setMaximumWidth(50)
        
    #-------------------------------------------
    def create_layout(self):
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        blank_layout = QtGui.QVBoxLayout()
        main_layout = QtGui.QHBoxLayout( self )
        main_layout.addLayout(blank_layout)
        main_layout.addLayout(layout)
        self.setLayout(layout)
        
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
    def create_connections(self):
        # Left click
        self.button1.released.connect( self.click )
        self.button2.pressed.connect( self.click )
        
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#    
    def click(self):
        
        button = self.sender()
        self.popup = Popup_Window( self, button )                   
        self.popup.show()
        


        
############################################
class Push_Buttons( QtGui.QPushButton ):
    def __init__( self ):
        super( Push_Buttons, self ).__init__()
        
        
        
############################################
class Popup_Window( QtGui.QWidget ):
    def __init__( self, parent, button ):
        super( Popup_Window, self ).__init__(parent)
        
        self.setWindowFlags(QtCore.Qt.Popup)
        
        self.button_pos = button       
        self.parent = parent  
                                              
        self.setAttribute( QtCore.Qt.WA_DeleteOnClose )
        self.resize(230, 100)
        
        self.installEventFilter(self)
        
        self.create_gui()
        self.create_layout()
        self.create_connections()
        self.move_UI()   
        self.line_edit.setFocus()     
        
    #-------------------------------------------
    def create_gui( self ):
        ''' Visible GUI stuff '''
        self.my_label = QtGui.QLabel("default text")
        self.line_edit = QtGui.QLineEdit()
        self.line_edit.setMaxLength( 30 )
        self.push_btn = QtGui.QPushButton( "push" )
        self.push_btn.setMaximumWidth( 30 )
        
    #-------------------------------------------
    def create_layout( self ):
        
        self.button_layout = QtGui.QVBoxLayout()
        
        self.button_layout.addWidget( self.my_label, 0, 0 )
        self.button_layout.addWidget( self.line_edit, 1, 0 )
        self.button_layout.addWidget( self.push_btn, 2, 0 )

        self.setLayout(self.button_layout)
        
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
    def create_connections( self ):
        
        self.line_edit.textChanged.connect( self.on_text_changed )
        
    #-----#-----#-----#-----#-----#-----#-----#-----#-----#
    def on_text_changed( self, text ): 
        
        #---- set the text in label ----
        typed_name = self.line_edit.text()
        if " " in typed_name:
            typed_name.replace(" ", "")
        self.my_label.setText(typed_name) 
            
    #-------------------------------------------  
    def  eventFilter(self, source, event):
        
        if event.type() == QtCore.QEvent.WindowDeactivate:
            self.close()
        return QtGui.QWidget.eventFilter(self, source, event)
        
    #-------------------------------------------
    def move_UI( self ):
        self.line_edit.setFocus()
        y_btn = self.button_pos.mapToGlobal(QtCore.QPoint(0,0)).y()  
        x_win = self.parent.mapToGlobal(QtCore.QPoint(0,0)).x()

        w_pop = self.frameGeometry().width()
        
        x = x_win - w_pop - 12
        y = y_btn

        self.move(QtCore.QPoint(x,y))

############################################
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