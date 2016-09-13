# Import modules into maya to begin
import maya.OpenMayaUI as omui 

# These two are the most common modules we'll be using
from PySide import QtCore 
from PySide import QtGui 

# The wrapInstance function allows you to convert pointers to python objects
from shiboken import wrapInstance 

# This function will return maya's main window qt widget
# It'll act as the parent of the new window
def maya_main_window():
    # First we need to get a pointer to that window
    # First we'll use the OpenMayaUI and from the MQtUtil class we'll be getting the main window
        # This is returning a pointer to maya's main window
    main_window_ptr = omui.MQtUtil.mainWindow()
    # We need to wrap this pointer using the wrap instance function
        # This will convert it to a python object
        # We cast the main_window_ptr to a long, the we tell it we want to wrap it as a QWidget object
        # QWidgets are fundamental elements in Qt
    return wrapInstance( long( main_window_ptr), QtGui.QWidget )

# Define the hello world function
def hello_world():
    # Creating the label of the window
    # Parent widget calls the maya_main_window() function
    label = QtGui.QLabel( "Hello World!", parent=maya_main_window() )
    # This will allow the label object to be displayed with the window's border on screen
    # QtCore.Qt.Window could also be QtCore.Qt.Tool
        # Tool is required for mac code so the window will always stay on top of the main window
        # It also has a different UI from a regular window for mac and pc users
    label.setWindowFlags( QtCore.Qt.Window )
    # Then show the label
    label.show()

# To execute this we just need to run the hello_world function
if __name__ == "__main__":
    hello_world()
    

    
""" Explanation of if __name__ == "__main__": statement:
    
# When your script is run by passing it as a command to the Python interpreter,

python myscript.py

# All of the code that is at indentation level 0 gets executed. 
# Functions and classes that are defined are, well, defined, but none of their code gets ran. 
# Unlike other languages, there's no main() function that gets run automatically - the main() function is implicitly all the code at the top level.

# In this case, the top-level code is an if block.  
# __name__ is a built-in variable which evaluate to the name of the current module.
# However, if a module is being run directly (as in myscript.py above), then __name__ instead is set to the string "__main__". 
# Thus, you can test whether your script is being run directly or being imported by something else by testing

if __name__ == "__main__":
    ...
    
# If that code is being imported into another module, the various function and class definitions will be imported, but the main() code won't get run.
# As a basic example, consider the following two scripts:

# file one.py
def func():
    print("func() in one.py")

print("top-level in one.py")

if __name__ == "__main__":
    print("one.py is being run directly")
else:
    print("one.py is being imported into another module")

# file two.py
import one

print("top-level in two.py")
one.func()

if __name__ == "__main__":
    print("two.py is being run directly")
else:
    print("two.py is being imported into another module")
    
# Now, if you invoke the interpreter as

python one.py

# The output will be

top-level in one.py
one.py is being run directly

# If you run two.py instead:

python two.py

# You get

top-level in one.py
one.py is being imported into another module
top-level in two.py
func() in one.py
two.py is being run directly

# Thus, when module one gets loaded, its __name__ equals "one" instead of __main__.
    
"""    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    