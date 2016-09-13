from PySide import QtCore, QtGui
from shiboken import wrapInstance
import maya.OpenMayaUI as mui
import maya.OpenMaya as om
import maya.cmds as mc
import maya.mel as mel
import os

def get_parent():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance( long( ptr ), QtGui.QWidget )   

class Main_Window(QtGui.QMainWindow):
    def __init__(self, parent=get_parent() ):
        super(Main_Window, self).__init__(parent)

        frame = QtGui.QFrame();
        frame.setLayout( QtGui.QHBoxLayout() );

        treeViewModel = TreeViewModel()
        treeView = Widget_TreeView(treeViewModel)
        frame.layout().addWidget( treeView );

        self.setCentralWidget(frame)
        
################################################################################
class TreeViewModel(QtCore.QAbstractItemModel):
    def __init__(self):
        super(TreeViewModel, self).__init__()
        
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(['Title', 'Summary'])
        rootItem = model.invisibleRootItem()
        
        #First top-level row and children 
        item0 = [QtGui.QStandardItem('Title0'), QtGui.QStandardItem('Summary0')]
        item00 = [QtGui.QStandardItem('Title00'), QtGui.QStandardItem('Summary00')]
        item01 = [QtGui.QStandardItem('Title01'), QtGui.QStandardItem('Summary01')]
        rootItem.appendRow(item0)
        item0[0].appendRow(item00)
        item0[0].appendRow(item01)

        #Second top-level item and its children
        item1 = [QtGui.QStandardItem('Title1'), QtGui.QStandardItem('Summary1')]
        item10 = [QtGui.QStandardItem('Title10'), QtGui.QStandardItem('Summary10')]
        item11 = [QtGui.QStandardItem('Title11'), QtGui.QStandardItem('Summary11')]
        item12 = [QtGui.QStandardItem('Title12'), QtGui.QStandardItem('Summary12')]
        rootItem.appendRow(item1)
        item1[0].appendRow(item10)
        item1[0].appendRow(item11)
        item1[0].appendRow(item12)

        #Children of item11 (third level items)
        item110 = [QtGui.QStandardItem('Title110'), QtGui.QStandardItem('Summary110')]
        item111 = [QtGui.QStandardItem('Title111'), QtGui.QStandardItem('Summary111')]
        item11[0].appendRow(item110)
        item11[0].appendRow(item111)
        
################################################################################
class Widget_TreeView(QtGui.QTreeView):
    def __init__(self, parent = get_parent() ):
        super(Widget_TreeView, self).__init__(parent)
        
        
        
        

############################################
if __name__ == "__main__":
    # Development stuff
    try:
        treeWidget.close()
        treeWidget.deleteLater()
    except:
        pass
    
    # Show stuff
    treeWidget = Main_Window()
    treeWidget.show()

    # Development stuff
    try:
        treeWidget.show()
    except:
        treeWidget.close()
        treeWidget.deleteLater()
