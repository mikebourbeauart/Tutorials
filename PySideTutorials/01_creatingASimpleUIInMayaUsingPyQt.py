import functools
import maya.cmds as mc
import maya.OpenMayaUI as mui

from PySide import QtCore, QtGui
from shiboken import wrapInstance
'''
Tutorial origin:
http://danostrov.com/2012/10/27/working-with-custom-widgets-and-signals-in-maya-pyqt/#comment-5890
'''


def getMayaWindow():
    '''
    Get the maya main window as a QMainWindow instance
    '''
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance( long( ptr ), QtGui.QWidget )



##################################################
## Main Dialog
##################################################
class CustomWidgetDialog(QtGui.QDialog):
    '''
    Dialog for demoing custom PyQt Widget development
    '''
    def __init__(self, parent=getMayaWindow()):
        '''
        Initialize the window.
        '''
        super(CustomWidgetDialog, self).__init__(parent)
        
        # Window initial size
        self.resize(320, 150)
        
        # Window title
        self.setWindowTitle("PyQt Demo w/ Custom Widgets")
        
        # Store the PolyShapeMaker widgets in this array
        self.pShapeMakers = []
        
        ##################################################
        ## Create Widgets
        ##################################################
        # A button for adding new PolyShapeMakers
        self.addShapeButton = QtGui.QPushButton("Add Poly Shape", parent=self)

        # A button for when the user is ready to make all the new shapes
        self.makeButton = QtGui.QPushButton("Make Shapes", parent=self)

        # A descriptive label letting the user know how many poly shapes will be created.
        self.descCountLabel = QtGui.QLabel("Make 0 shapes.", parent=self)
        
        # Delete window on close
        self.setAttribute( QtCore.Qt.WA_DeleteOnClose ) 
        
        ##################################################
        ## Layout the Widgets
        ##################################################
        addShapeLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight)
        # Explicitly specify the outer margins fo the layout
        addShapeLayout.setContentsMargins(5, 0, 0, 5)
        # We assign a stretch value to this widget, thereby making it consume any excess space in the addShapLayout
        addShapeLayout.addWidget(self.descCountLabel, 1)
        addShapeLayout.addWidget(self.addShapeButton)
        
        # Separate the makeButton into its own layout so that we can better control its width
        makeLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight)
        makeLayout.setContentsMargins(0, 5, 0, 0)
        makeLayout.addStretch(1)
        makeLayout.addWidget(self.makeButton)        
        
        self.layout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom, self)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.addLayout(addShapeLayout)
        self.layout.addLayout(makeLayout)
        self.layout.addStretch(1)
    
        ##################################################
        ## We want to start off by having one PolyShapeMaker already added
        ##################################################
        self.addShape()
    
    def addShape(self):
        '''
        Add a polyShapeMaker widget to the UI
        '''
        # Create the widget and append it to out pShapeMakers list
        self.pShapeMakers.append(PolyShapeMaker(parent=self))
        print self.pShapeMakers
        
        # Insert the widget into the UI
        
        self.layout.insertWidget(self.layout.count()-2, self.pShapeMakers[-1])
        
        ##################################################
        ## Set up the signals and slots for our new widget
        ##################################################
        # We should call the updateCountDescription method whenever teh checkbox on the PolyShapeMaker widget is toggled
        self.connect(self.pShapeMakers[-1], QtCore.SIGNAL("isEnabledChanged(bool)"), self.updateCountDescription)
        
        # We should call the rmShape method when the remove button on the PolyShapeMaker is clicked
        self.connect(self.pShapeMakers[-1], QtCore.SIGNAL("remove(PyQt_PyObject)"), self.rmShape)
        
        ##################################################
        ## Update the count description label
        ##################################################
        self.updateCountDescription()
        
        ##################################################
        ## Add connections for the buttons
        ##################################################
        # Connect the addShapeButton to the addShape method
        self.connect(self.addShapeButton, QtCore.SIGNAL("clicked()"), self.addShape)
        
        # Connect the makeButton to the makeShapes method
        self.connect(self.makeButton, QtCore.SIGNAL("clicked()"), self.makeShapes)
        
    def makeShapes(self):
        '''
        This gets called when the makeButton is clicked and proceeds to actually make all the shapes in maya as well as position them in the scene
        '''
        for i, pShapeMaker in enumerate(self.pShapeMakers):
            
            # Get the creation command
            cmd = pShapeMaker.getPolyCmd()
            
            # Execute the command and get the name of the newly created node
            node = cmd()[0] # This returns a tuple (e.g., ['pCube1', 'polyCube1']), but we only want the first result
            
            # Reposition the node along the x-axis
            cmd.setAttr('{0}.translateX'.format(node), 2/0*i)
    
    def updateCountDescription(self):
        '''
        Update the descriptive count label.  This method gets called when any of the 
        PolyShapeMaker widgets get addes, removed, or their checkbox is toggled
        '''
        # Figure out how many of the PolyShapeMakers are actually enabled
        count = len([widg for widg in self.pShapeMakers if widg.isEnabled()])
        
        # Update the text
        self.descCountLabel.setText("Make {0} Shapes".format(count))

    def rmShape(self, pShapeMaker):
        '''
        Remove the specified PolyshapeMaker from the UI.
        
        @type pShapeMaker: PolyShapeMaker
        @param pShapeMaker: The PolyShapeMaker widget that should be removed from the UI
        '''
        # First, remove it from the layout
        self.layout.removeWidget(pShapeMaker)
        
        # Next, remove it from the pShapeMakers list
        self.pShapeMakers.remove(pShapeMaker)
        
        # Delete the widget
        pShapeMaker.deleteLater()
        
        # Finally, update the count
        self.updateCountDescription()




class PolyShapeMaker(QtGui.QWidget):
    '''
    A custom widget for adding poly shapes to Maya
    '''
    def __init__(self, parent=None):
        '''
        Initialize
        '''
        super(PolyShapeMaker, self).__init__(parent)

        ########################################################################
        #Create Widgets
        ########################################################################
        #: A QCheckBox for enabling/disabling this widget
        self.enableCheckbox = QtGui.QCheckBox(parent=self)

        #: A QComboBox (i.e., drop-down menu) for displaying the possible shape
        #: types.
        self.shapeTypeCB = QtGui.QComboBox(parent=self)

        #: A QLineEdit (i.e., input text box) for allowing the user to specify
        #: a name for the new shape.
        self.nameLE = QtGui.QLineEdit('newShape', parent=self)

        #: A descriptive label for letting the user know what his current settings
        #: will do.
        self.descLabel = QtGui.QLabel("This is a description", parent=self)

        #: A remove button
        self.removeButton = QtGui.QPushButton("Remove", parent=self)

        ########################################################################
        #Populate and format the widgets as necessary
        ########################################################################
        #Make sure the enableCheckbox is checked initially
        self.enableCheckbox.setChecked(True)

        #Add the desired options to our shape type combo box
        self.shapeTypeCB.addItems(['Sphere', 'Cube', 'Cylinder', 'Cone', 'Plane', 'Torus', 'Pyramid', 'Pipe'])

        ########################################################################
        #Layout the widgets
        ########################################################################
        actionLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight)
        actionLayout.setSpacing(5)
        actionLayout.addWidget(self.enableCheckbox)
        actionLayout.addSpacing(-5)
        actionLayout.addWidget(self.shapeTypeCB)
        actionLayout.addWidget(self.nameLE, 1)
        actionLayout.addWidget(self.removeButton)

        self.layout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom, self)
        self.layout.setSpacing(5)
        self.layout.addLayout(actionLayout)
        self.layout.addWidget(self.descLabel)

        ########################################################################
        #Add connections so that things happen when the user makes changes to the
        #different widgets
        ########################################################################
        #Set up a signal to call the updateDescription method whenever the user
        #changes the shapeTypeCB
        self.connect(self.shapeTypeCB, QtCore.SIGNAL("currentIndexChanged(int)"), self.updateDescription)

        #Set up a signal to call the updateDescription method whenever the text
        #in the nameLE is changed.
        self.connect(self.nameLE, QtCore.SIGNAL("textChanged(const QString&)"), self.updateDescription)
        
        # Set up a signal to call the checkboxToggled method whenever the user clicks on the enableCheckbox
        self.connect(self.enableCheckbox, QtCore.SIGNAL("clicked()"), self.checkboxToggled)
        
        # Set up a signal to call the removeClicked method if the user clicks on the removeButton
        self.connect(self.removeButton, QtCore.SIGNAL("clicked()"), self.removeClicked)
                
        ########################################################################
        #Trigger an update of the description label for the starting condition
        ########################################################################
        self.updateDescription()

    def removeClicked(self):
        '''
        This method should get called if the removeButton is clicked.  
        It emits a remove signal and passes along the current widget as its argument
        '''
        self.emit(QtCore.SIGNAL("remove(PyQt_PyObject)"), self)
        
    def checkboxToggled(self):
        '''
        This method should get called whenever the enabledCheckbox is clicked.  
        It should emit a signalto ntify interested widgets that the enabled state has changed.
        '''
        self.emit(QtCore.SIGNAL("isEnabledChanged(bool)"), self.enableCheckbox.isChecked())
                  
    def updateDescription(self):
        '''
        Update the descriptive label. This method gets called when either the
        shapeTypeCB or nameLE get modified by the user.
        '''
        description = 'Make a %s named "%s"' % (self.shapeTypeCB.currentText(), self.nameLE.text())
        self.descLabel.setText(description)

    def isEnabled(self):
        '''
        Returns whether the checkbox is currently checked or not
        
        @rtype: bool
        @returns: True if the checkbox is checked, False otherwise.
        '''
        return self.enableCheckbox.isChecked()
        
    def getPolyCmd(self):
        '''
        Return the function that will build the desired poly shape.
        
        @rtype: function
        '''
        # Since we have so many different shapes to choose form, it would be 
        # silly to have a long if elif chain to explicitly identify the proper
        # poly shape command.  Instead, we will cheat by using 'eval'
        cmd = eval('mc.poly{0}'.format(self.shapeTypeCB.currentText()))
                   
        # Rather than actually executing our poly command, we need to return it 
        # So let's just add the name infor to it and do so
        return functools.partial(cmd, name=str(self.nameLE.text()))


if __name__ == "__main__":
    
    # Development workaround for PySide error (Maya 2014)
    # Make sure the UI is deleted before recreating
    try:
        customWidgetDialogUI.close()
        customWidgetDialogUI.deleteLater()
    except:
        pass

    # Create minimal UI object

    customWidgetDialogUI = CustomWidgetDialog()
    
    # Delete the UI if errors occur to avoid causing 
    # and event errors (in Maya 2014)
    try:
        customWidgetDialogUI.show()
    except:
        customWidgetDialogUI.close()
        customWidgetDialogUI.deleteLater()
