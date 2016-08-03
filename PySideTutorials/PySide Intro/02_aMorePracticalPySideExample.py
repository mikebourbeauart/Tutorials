from PySide import QtCore  
from PySide import QtGui  
from shiboken import wrapInstance  
import maya.cmds as mc 
import maya.OpenMayaUI as omui 
 
# This is unchanged from the last lesson 
    # This will return the QWidget and allow us to parent the tool to maya's main window only 
def maya_main_window(): 
    main_window_ptr = omui.MQtUtil.mainWindow() 
    return wrapInstance( long( main_window_ptr), QtGui.QWidget ) 
 
#Create a new class called PrimitiveUi 
    #This will be extending the QDialog class 
class PrimitiveUi( QtGui.QDialog ): 
    # Create the initialization method and pass in the parent widget 
        # By default make it pass the maya_main_window function 
    def __init__( self, parent=maya_main_window()): 
        # Pass in a parent class and pass in a parent object 
        super( PrimitiveUi, self ).__init__( parent ) 
         
        # Because we're extending the Qdialog class we have access to all the QDialog methods 
        # Give it a title 
        self.setWindowTitle( "Primitives" ) 
        # Make the window a tool window so it stays on top of maya 
        self.setWindowFlags( QtCore.Qt.Tool ) 
        # Delete UI on close to avoid errors 
        self.setAttribute( QtCore.Qt.WA_DeleteOnClose ) 
        # This function places the items from it into the layout 
        self.create_layout() 
         
        self.create_connections() 
     
    # New method called create_layout 
        # This is where any of the layout code is going to be placed 
    def create_layout( self ): 
        # Create out buttons and give it a label that you'll see on the button 
            # You won't see any changes at first because you need to call the self.create_layout method within the __init__ function 
        self.cube_btn = QtGui.QPushButton( "Cube" ) 
        self.sphere_btn = QtGui.QPushButton( "Sphere" ) 
        self.cone_btn = QtGui.QPushButton( "Cone" ) 
        self.cylinder_btn = QtGui.QPushButton( "Cylinder" ) 
         
        # Create a layout  
        main_layout = QtGui.QVBoxLayout() 
        # Set margin values and spacing 
        main_layout.setContentsMargins( 2, 2, 2, 2 ) 
        main_layout.setSpacing( 2 ) 
        # Add the widgets to the layout 
        main_layout.addWidget( self.cube_btn ) 
        main_layout.addWidget( self.sphere_btn ) 
        main_layout.addWidget( self.cone_btn ) 
        main_layout.addWidget( self.cylinder_btn ) 
        # Prevent buttons from moving down when window is resized vertically 
        main_layout.addStretch() 
         
        # Add the main_layout itself to the PrimitiveUi dialog 
        self.setLayout( main_layout ) 
     
    # This will be our first look at signals and slots using PySide 
        # We'll be connecting the button clicked signal with each of the methods that we've created below 
    def create_connections( self ): 
        self.cube_btn.clicked.connect( PrimitiveUi.make_cube ) 
        self.sphere_btn.clicked.connect( PrimitiveUi.make_sphere ) 
        self.cone_btn.clicked.connect( PrimitiveUi.make_cone ) 
        self.cylinder_btn.clicked.connect( PrimitiveUi.make_cylinder ) 
         
    # Class methods 
    # function make_cube calling the maya polyCube command 
    @classmethod 
    def make_cube( cls ): 
        mc.polyCube() 
         
    @classmethod 
    def make_sphere( cls ): 
        mc.polySphere() 
         
    @classmethod 
    def make_cone( cls ): 
        mc.polyCone() 
         
    @classmethod 
    def make_cylinder( cls ): 
        mc.polyCylinder() 
     
     
if __name__ == "__main__": 
     
    try: 
        ui.close() 
    except: 
        pass 
     
    # Create an instance of PrimitiveUi 
    ui = PrimitiveUi() 
    # Show the window 
    ui.show() 