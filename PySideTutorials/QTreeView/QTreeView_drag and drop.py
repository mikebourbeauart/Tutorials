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

        self.treeModel = TreeModel()

        self.view = Widget_TreeView( self.treeModel )
        self.view.setDragDropMode(QtGui.QAbstractItemView.InternalMove)

        self.setCentralWidget(self.view)
        
################################################################################
class Widget_TreeView(QtGui.QTreeView):
    #---------------------------------------------------------------------------
    def __init__(self, model, parent=None):
        super(Widget_TreeView, self).__init__(parent)
        self.setModel(model)

        
class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self):
        QtCore.QAbstractItemModel.__init__(self)
        self.nodes = ['node0', 'node1', 'node2']

    def index(self, row, column, parent):
        return self.createIndex(row, column, self.nodes[row])

    def parent(self, index):
        return QtCore.QModelIndex()

    def rowCount(self, index):
        if index.internalPointer() in self.nodes:
            return 0
        return len(self.nodes)

    def columnCount(self, index):
        return 1

    def data(self, index, role):
        if role == 0: 
            return index.internalPointer()
        else:
            return None

    def supportedDropActions(self): 
        return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction         

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled        

    def mimeTypes(self):
        return ['text/xml']

    def mimeData(self, indexes):
        mimedata = QtCore.QMimeData()
        mimedata.setData('text/xml', 'mimeData')
        return mimedata

    def dropMimeData(self, data, action, row, column, parent):
        print 'dropMimeData %s %s %s %s' % (data.data('text/xml'), action, row, parent) 
        return True


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

