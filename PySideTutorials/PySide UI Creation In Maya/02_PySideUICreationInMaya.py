from PySide import QtGui
import maya.OpenMayaUI as mui
import shiboken
import maya.cmds as cmd

def getMayaWindow():
    pointer = mui.MQtUtil.mainWindow()
    return shiboken.wrapInstance( long(pointer), QtGui.QWidget )

def createConstraintLayout( attribute, parentLayout, checked ):
    # Create and add the horizontal layout
    layout = QtGui.QHBoxLayout()
    parentLayout.addLayout( layout )    
    
    # Create label
    label = QtGui.QLabel( attribute )
    layout.addWidget( label )    
    
    # Create font and assign
    font = QtGui.QFont()
    font.setPointSize( 10 )
    font.setBold( True )
    label.setFont( font )
    
    # Add spacer
    spacer = QtGui.QSpacerItem( 30, 0 )
    layout.addSpacerItem( spacer )
    
    # Loop through attributes and create a checkbox for each one
    for attr in ["X", "Y", "Z"]:
        checkbox = QtGui.QCheckBox( attr )
        objectName = attribute.partition(":")[0] + attr +"_cmCheckBox"
        checkbox.setObjectName( objectName )
        checkbox.setChecked( checked )
        layout.addWidget( checkbox )
        checkbox.setMinimumWidth( 30 )
        checkbox.setMaximumWidth( 30 )
        
    # Create spacer and maintain offsets checkbox
    spacer = QtGui.QSpacerItem( 10, 0 )
    layout.addSpacerItem( spacer )
    
    offsetCheckbox = QtGui.QCheckBox( "Maintain Offsets" )
    objectName = attribute.partition(":")[0] + "_cmCheckBox_offset"
    offsetCheckbox.setObjectName( objectName )
    layout.addWidget( offsetCheckbox )
    
def createConstraint():
    # Get selection
    selection = cmd.ls( sl=True )
    if len(selection) > 0:
        constraintObj = selection[0]
        targetObj = selection[1]
    
    # Get checkbox values
    for attribute in ["Translate", "Rotate", "Scale"]:
        skipList = []
        
        # Get checkbox values
        for attr in ["X", "Y", "Z"]:
            if cmd.control( attribute + attr + "_cmCheckBox", exists=True ):
                ptr = mui.MQtUtil.findControl( attribute + attr + "_cmCheckBox" )
                checkBox = shiboken.wrapInstance( long( ptr ), QtGui.QCheckBox )
                value = checkBox.isChecked()
                if not value:
                    skipList.append( attr.lower() )
         
        maintainOffset = False
        
        # Maintain offsets
        if cmd.control( attribute + "_cmCheckBox_offset", exists=True ):
            ptr = mui.MQtUtil.findControl( attribute + "_cmCheckBox_offset" )
            checkBox = shiboken.wrapInstance( long( ptr ), QtGui.QCheckBox )
            maintainOffset = checkBox.isChecked()
            
        # Create constraint
        if len(skipList) != 3:
            if attribute == "Translate":
                cmd.pointConstraint( constraintObj, targetObj, skip=skipList, mo=maintainOffset )         
            if attribute == "Rotate":
                cmd.orientConstraint( constraintObj, targetObj, skip=skipList, mo=maintainOffset )
            if attribute == "Scale":
                cmd.scaleConstraint( constraintObj, targetObj, skip=skipList, mo=maintainOffset )

def constraintMaster_UI():
    objectName = "pyConstraintMasterWin"
    
    # Check to see if the UI already exists and if so, delete
    if cmd.window( "pyConstraintMasterWin", exists=1 ):
        cmd.deleteUI( "pyConstraintMasterWin", wnd=1 )
        
    # Create the window
    parent = getMayaWindow()
    window = QtGui.QMainWindow( parent )
    window.setObjectName( objectName )
    window.setWindowTitle( "Constraint Master" )
    window.setMinimumSize( 400, 125 )
    window.setMaximumSize( 400, 125 )
    
    # Create the main widget
    mainWidget = QtGui.QWidget()
    window.setCentralWidget( mainWidget )
    
    # Create our main vertical layout
    verticalLayout = QtGui.QVBoxLayout( mainWidget )
    
    # Loop through the attributes, create layout
    for attribute in ["Translate:", "Rotate:", "Scale:"]:
        if attribute == "Scale:":
            createConstraintLayout( attribute, verticalLayout, False )
        else:
            createConstraintLayout( attribute, verticalLayout, True )
    
    # Create the "create" button
    button = QtGui.QPushButton( "Create Constraint" )
    verticalLayout.addWidget( button )
    button.clicked.connect( createConstraint )
    # Create our main vertical layout
    verticalLayout = QtGui.QVBoxLayout( mainWidget )
    # Show the window
    window.show()
    
constraintMaster_UI()
























