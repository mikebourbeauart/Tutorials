########################################################################################################################
#
# mb_pandora
# By Mike Bourbeau
# mikebourbeau.com
# 2015
#
# Big thanks to Chris Zurbrigg (especially for taking the time to answer all my questions and steer me in the right direction),
# Jeremy Ernst, Cesar Saez, and all other tutorial makers/educators online
#
########################################################################################################################

from PySide import QtCore, QtGui
from shiboken import wrapInstance 
import maya.OpenMayaUI as mui
import maya.OpenMaya as om
import maya.cmds as mc
import maya.mel as mel
import inspect

def get_parent():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance( long( ptr ), QtGui.QWidget )   
    
def show():
    m = PandoraUI(parent=get_parent())
    m.exec_()
    del m
    
########################################################################################################################
class PandoraUI( QtGui.QDialog ):
    ''' Create the text field that the user types into '''
    def __init__( self, parent=get_parent() ):
        super( PandoraUI, self ).__init__(  )
        
        # Commands
        self.move_UI()
        self.create_gui()
        self.create_layout()
        self.create_connections()
        self.setAttribute( QtCore.Qt.WA_DeleteOnClose ) 

    def move_UI(self):
        ''' Moves the UI to the cursor's position '''
        pos = QtGui.QCursor.pos()
        self.move(pos.x()-100, pos.y()+25)
        self.setFixedSize(230, 30)

    def create_gui( self ):
        ''' Visible GUI '''
        # Hide window stuff
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # Line edit 
        self.line_edit = Line_Edit(parent=self)
        # Completer AKA view
        self.completer = QtGui.QCompleter(self)
        self.completer.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer.setMaxVisibleItems(15)
        # ProxyModel 
        self.pFilterModel = QtGui.QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        # Set completer
        self.line_edit.setCompleter(self.completer)

    def set_model(self, model):
        ''' Set model '''
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)
        self.completer.setModelSorting(QtGui.QCompleter.CaseInsensitivelySortedModel)

    def create_layout( self ):
        ''' Create layout '''
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.addWidget( self.line_edit )
        main_layout.totalMaximumSize()
        main_layout.setContentsMargins(2,2,2,2)
        self.setLayout( main_layout )
    
    def create_connections( self ):
        ''' Connections '''
        self.line_edit.textEdited[unicode].connect(self.pFilterModel.setFilterFixedString)
        self.line_edit.returnPressed.connect( self.on_text_edited )
        self.line_edit.esc_pressed.connect( self.on_esc_press )
        self.line_edit.tab_pressed.connect( self.on_text_edited )
        self.line_edit.mouse_pressed.connect( self.on_esc_press )
    
    ####################################################################################################################
    ## SLOTS   
    ####################################################################################################################
    
    def on_text_edited(self):
        ''' Run this when text is edited to execute a command '''
        command_list = []
        for name, data in inspect.getmembers(mc, callable):
            command_list.append(name)
        command = self.line_edit.text()
        if len( command ):
            if command in command_list:
                mel_command = mel.eval( "{0}".format( command ) )
                self.close()
            else:
                om.MGlobal.displayError("Not a valid command")
        else:
            om.MGlobal.displayInfo("")
            self.close()

    def on_esc_press(self):
        ''' Close the UI '''
        om.MGlobal.displayInfo("")
        self.close()
        
########################################################################################################################
class Line_Edit( QtGui.QLineEdit ):
    ''' Create the QLineEdit '''
    # Signal Variables
    esc_pressed = QtCore.Signal(str)
    esc_signal_str = "escPressed"
    tab_pressed = QtCore.Signal(str)
    tab_signal_str = "tabPressed"
    mouse_pressed = QtCore.Signal(str)
    mouse_signal_str = "mousePressed"
    
    def __init__(self, parent=None):
        super( Line_Edit, self ).__init__(  )
        
        # Sizing the line edit
        self.setFixedHeight(25)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        self.setFont(font)

    # Custom Signals
    def event(self, event):
        if (event.type()==QtCore.QEvent.KeyPress):
            if (event.key()==QtCore.Qt.Key_Escape):
                self.esc_pressed.emit(self.esc_signal_str)
                return True
            if (event.key()==QtCore.Qt.Key_Tab):
                self.tab_pressed.emit(self.tab_signal_str)
                return True
            return QtGui.QLineEdit.event(self, event)
        if (event.type()==QtCore.QEvent.FocusOut):
            self.mouse_pressed.emit(self.mouse_signal_str)
            return True
        return QtGui.QLineEdit.event(self, event)
            





########################################################################################################################
if __name__ == "__main__":
#def run():

# Development stuff
    try:
        pandora_ui.close()
        pandora_ui.deleteLater()
    except:
        pass
    
    # Get commands
    command_list = []
    for name, data in inspect.getmembers(mc, callable):
        command_list.append(name)

    # Set items in model
    model = QtGui.QStandardItemModel()
    for i,word in enumerate(command_list):
        item = QtGui.QStandardItem(word)
        model.setItem(i, item)

    # Action stuff
    pandora_ui = PandoraUI()
    pandora_ui.show()
    pandora_ui.set_model(model)

    # Development stuff
    try:
        pandora_ui.show()
    except:
        pandora_ui.close()
        pandora_ui.deleteLater()

   