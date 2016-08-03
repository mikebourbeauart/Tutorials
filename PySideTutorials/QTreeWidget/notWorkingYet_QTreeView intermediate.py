from PySide import QtCore, QtGui
from shiboken import wrapInstance
import maya.OpenMayaUI as mui
import sys, os


def get_parent():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance( long( ptr ), QtGui.QWidget )  

################################################################################
class Main_Window(QtGui.QMainWindow):
    def __init__(self, parent=get_parent() ):
        super(Main_Window, self).__init__(parent)

        # Trying to get it to work

        frame = QtGui.QFrame();
        frame.setLayout( QtGui.QHBoxLayout() );

        treeViewModel = NamesModel( data )
        treeView = Widget_TreeView(treeViewModel)
        frame.layout().addWidget( treeView );

        self.setCentralWidget(frame)

#-------------------------------------------------------------------------------
class TreeNode(object):
    def __init__(self, parent, row):
        self.parent = parent
        self.row = row
        self.subnodes = self._getChildren()

    def _getChildren(self):
        raise NotImplementedError()

################################################################################
class Widget_Tree_Model(QtCore.QAbstractItemModel):
    def __init__(self):
        QtCore.QAbstractItemModel.__init__(self)
        self.rootNodes = self._getRootNodes()

    def _getRootNodes(self):
        raise NotImplementedError()

    def index(self, row, column, parent):
        if not parent.isValid():
            return self.createIndex(row, column, self.rootNodes[row])
        parentNode = parent.internalPointer()
        return self.createIndex(row, column, parentNode.subnodes[row])

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        node = index.internalPointer()
        if node.parent is None:
            return QModelIndex()
        else:
            return self.createIndex(node.parent.row, 0, node.parent)

    def reset(self):
        self.rootNodes = self._getRootNodes()
        QtCore.QAbstractItemModel.reset(self)

    def rowCount(self, parent):
        if not parent.isValid():
            return len(self.rootNodes)
        node = parent.internalPointer()
        return len(node.subnodes)

################################################################################
class Widget_Tree_View(QtGui.QTreeView):
    def __init__(self, model, parent=None):
        super(Widget_Tree_View, self).__init__(parent)
        
        self.setModel(model)
        model.setView(self)
        root = model.index(0, 0)
        
#-------------------------------------------------------------------------------
class NamedElement(object): # your internal structure
    def __init__(self, name, subelements):
        self.name = name
        self.subelements = subelements
        
#-------------------------------------------------------------------------------
class NamedNode(TreeNode):
    def __init__(self, ref, parent, row):
        self.ref = ref
        TreeNode.__init__(self, parent, row)

    def _getChildren(self):
        return [NamedNode(elem, self, index)
            for index, elem in enumerate(self.ref.subelements)]
        
#-------------------------------------------------------------------------------
class NamesModel(Widget_Tree_Model):
    def __init__(self, rootElements):
        self.rootElements = rootElements
        Widget_Tree_Model.__init__(self)

    def _getRootNodes(self):
        return [NamedNode(elem, None, index)
            for index, elem in enumerate(self.rootElements)]

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == Qt.DisplayRole and index.column() == 0:
            return node.ref.name
        return None

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole and section == 0:
            return 'Name'
        return None


################################################################################
if __name__ == '__main__':
    try:
        form_ui.close()
        form_ui.deleteLater()
    except:
        pass
        
    form_ui = Main_Window()
    form_ui.show()

    try:
        form_ui.show()
    except:
        form_ui.close()
        form_ui.deleteLater()