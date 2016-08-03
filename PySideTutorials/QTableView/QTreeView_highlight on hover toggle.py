from PySide import QtCore, QtGui
import maya.OpenMayaUI as mui
from shiboken import wrapInstance 

def get_parent():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance( long( ptr ), QtGui.QWidget )
    
class TableViewer(QtGui.QMainWindow):
    def __init__(self, parent=get_parent()):
        super(TableViewer, self).__init__(parent)
        self.table = QtGui.QTableWidget(3, 3)
        for row in range (0,3):
            for column in range(0,3):
                item = QtGui.QTableWidgetItem("This is cell {} {}".format(row+1, column+1))
                self.table.setItem(row, column, item)
        self.setCentralWidget(self.table)

        self.table.setMouseTracking(True)

        self.current_hover = [0, 0]
        self.table.cellEntered.connect(self.cellHover)

    def cellHover(self, row, column):
        item = self.table.item(row, column)
        old_item = self.table.item(self.current_hover[0], self.current_hover[1])
        if self.current_hover != [row,column]:
            old_item.setBackground(QtGui.QBrush(QtGui.QColor('white')))
            item.setBackground(QtGui.QBrush(QtGui.QColor('yellow')))
        self.current_hover = [row, column]


############################################
if __name__ == '__main__':
    # Things to fix PySide Maya bug
    try:
        tv_ui.close()
        tv_ui.deleteLater()
    except:
        pass
        
    tv_ui = TableViewer()
    tv_ui.show()

    try:
        tv_ui.show()
    except:
        tv_ui.close()
        tv_ui.deleteLater()