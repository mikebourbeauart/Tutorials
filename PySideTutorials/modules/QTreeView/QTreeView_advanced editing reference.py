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

        data = MyData.init()
        frame = QtGui.QFrame();
        frame.setLayout( QtGui.QHBoxLayout() );

        treeViewModel = Widget_Tree_Model(data)
        treeView = Widget_Tree_View(treeViewModel)
        frame.layout().addWidget( treeView );

        self.setCentralWidget(frame)

################################################################################
# my test data
class MyData():
    def __init__(self, txt, parent=None):
        self.txt = txt
        self.tooltip = None
        self.parent = parent
        self.child = []
        self.icon = []
        self.index = None
        self.widget = None

    #---------------------------------------------------------------------------
    def position(self):
        position = 0
        if self.parent is not None:
            count = 0
            children = self.parent.child
            for child in children:
                if child == self:
                    position = count
                    break
                count += 1
        return position

    #---------------------------------------------------------------------------
    # test initialization
    @staticmethod
    def init():
        root = MyData("root")
        root.tooltip = "root tooltip"
        for i in range(0, 2):
            child1 = MyData("child %i" % (i), root)
            child1.tooltip = "child1 tooltip"
            root.child.append(child1)
            for x in range(0, 2):
                child2 = MyData("child %i %i" % (i, x), child1)
                child2.tooltip = "child2 tooltip"
                child1.child.append(child2)

        return root
        

################################################################################
class Widget_Tree_Model(QtCore.QAbstractItemModel):
    #---------------------------------------------------------------------------
    def __init__(self, tree):
        super(Widget_Tree_Model, self).__init__()
        self.__tree = tree
        self.__view = None

    #---------------------------------------------------------------------------
    def flags(self, index):
        flag = QtCore.Qt.ItemIsEnabled
        if index.isValid():
            flag |= QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable 
        return flag

    #---------------------------------------------------------------------------
    def index(self, row, column, parent=QtCore.QModelIndex()):
        node = QtCore.QModelIndex()
        if parent.isValid():
            nodeS = parent.internalPointer()
            nodeX = nodeS.child[row]
            node = self.__createIndex(row, column, nodeX)
        else:
            node = self.__createIndex(row, column, self.__tree)
        return node

    #---------------------------------------------------------------------------
    def parent(self, index):
        return QtCore.QModelIndex()
    #---------------------------------------------------------------------------
    def rowCount(self, index=QtCore.QModelIndex()):
        count = 1
        node = index.internalPointer()
        if node is not None:
            count = len(node.child)
        return count

    #---------------------------------------------------------------------------
    def columnCount(self, index=QtCore.QModelIndex()):
        return 2

    #---------------------------------------------------------------------------
    def data(self, index, role=QtCore.Qt.DisplayRole):
        data = None
        return data

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
class Widget_Tree_View(QtGui.QTreeView):
    #---------------------------------------------------------------------------
    def __init__(self, model, parent=None):
        super(Widget_Tree_View, self).__init__(parent)
        
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

