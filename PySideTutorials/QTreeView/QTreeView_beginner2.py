from PySide import QtCore, QtGui
from shiboken import wrapInstance
import maya.OpenMayaUI as mui
import sys, os


def get_parent():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance( long( ptr ), QtGui.QWidget )  

class Main(QtGui.QDialog):

    def __init__(self, parent=get_parent() ):
        super(Main, self).__init__(parent)
        
        self.create_view()
        self.set_model( None )
        self.create_layout()
        self.set_connections()
    
    def set_model(self, model):
        self.tv_file_list.model = QtGui.QFileSystemModel()
        self.tv_file_list.model.setRootPath( QtCore.QDir.currentPath() )
        self.tv_file_list.setModel(self.tv_file_list.model)
    
    def create_view( self ):
        self.tv_file_list = QtGui.QTreeView()
    
    def create_layout( self ):
        main_layout = QtGui.QVBoxLayout( self )
        main_layout.addWidget( self.tv_file_list )
        self.setLayout( main_layout )
        
    def set_connections( self ):
        self.tv_file_list.selectionModel()
        QtCore.QObject.connect(self.tv_file_list.selectionModel(), QtCore.SIGNAL('selectionChanged(QItemSelection, QItemSelection)'), self.test)


    @QtCore.Slot("QItemSelection, FQItemSelection")
    def test(self, selected, deselected):
        print("hello!")
        print(selected)
        print(deselected)

################################################################################
class TreeViewModel(QtCore.QAbstractItemModel):
    #---------------------------------------------------------------------------
    def __init__(self, tree):
        super(TreeViewModel, self).__init__()
        
        
################################################################################
class Widget_TreeView(QtGui.QTreeView):
    #---------------------------------------------------------------------------
    def __init__(self, model, parent=None):
        super(Widget_TreeView, self).__init__(parent)
        self.setModel(model)
        model.setView(self)
        root = model.index(0, 0)

################################################################################
class Widget_Tooltip(QtGui.QWidget):
    #---------------------------------------------------------------------------
    def __init__(self, node):
        super(Widget_Tooltip, self).__init__()
        
        # Vars
        self.node = node
        self.txt = None
        # Commands
        self.create_tooltip(self.node)

    ############################################
    def create_tooltip(self, node):
        layout = QtGui.QHBoxLayout()
        self.txt = QtGui.QLabel( node.txt)
        self.txt.setToolTip("Text tooltip %s %s" % (node.txt, node.tooltip))
        layout.addWidget(self.txt, 1)
        self.setLayout(layout)
        
        
        
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    try:
        form_ui.close()
        form_ui.deleteLater()
    except:
        pass
        
    form_ui = Main()
    form_ui.show()

    try:
        form_ui.show()
    except:
        form_ui.close()
        form_ui.deleteLater()