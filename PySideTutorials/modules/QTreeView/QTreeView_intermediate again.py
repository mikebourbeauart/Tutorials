from PySide import QtCore, QtGui
from shiboken import wrapInstance
import maya.OpenMayaUI as mui
import sys, os


def get_parent():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance( long( ptr ), QtGui.QWidget )   


class MainForm(QtGui.QMainWindow):
    def __init__(self, parent=get_parent() ):
        super(MainForm, self).__init__(parent)
        
        data = ['file1', 'file2', 'file3','a', 'b', 'c']
        
        self.treeModel = TreeModel( data )

        self.view = Widget_TreeView( self.treeModel )

        self.setCentralWidget(self.view)
        
################################################################################
class Widget_TreeView(QtGui.QTreeView):
    def __init__(self, model, parent=None):
        super(Widget_TreeView, self).__init__(parent)
        
        self.setModel(model)
        model.setView( self )
        root = model.index(0,0)
        
################################################################################
class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, tree):
        QtCore.QAbstractItemModel.__init__(self)
        self.__tree = tree
        
    def index(self, row, column, parent=QtCore.QModelIndex() ):
        node = QtCore.QModelIndex()
        #node = self.__createIndex(row, column, self.__tree)
        return self.createIndex(row, column, self.__tree[row])

    def parent(self, index):
        return QtCore.QModelIndex()

    def rowCount(self, index):
        if index.internalPointer() in self.__tree:
            return 0
        return len(self.__tree)

    def columnCount(self, index=QtCore.QModelIndex()):
        return 2

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == 0: 
            return index.internalPointer()
        else:
            return None
     
    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable   
    
    #---------------------------------------------------------------------------
    def setView(self, view):
        self.__view = view
        
    #---------------------------------------------------------------------------
    def __createIndex(self, row, column, node):
        if node.index == None:
            index = self.createIndex(row, column, node)
            node.index = index
        if node.widget is None:
            node.widget = Widget_Tooltip(node)
            self.__view.setIndexWidget(index, node.widget)
        return node.index



################################################################################
class Widget_Tooltip(QtGui.QWidget):
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

if __name__ == '__main__':
    try:
        form_ui.close()
        form_ui.deleteLater()
    except:
        pass
        
    form_ui = MainForm()
    form_ui.show()

    try:
        form_ui.show()
    except:
        form_ui.close()
        form_ui.deleteLater()

