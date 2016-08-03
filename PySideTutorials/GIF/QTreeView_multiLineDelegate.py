import sys
from PySide import QtGui, QtCore

class SimpleTree(QtGui.QTreeView):
    def __init__(self, parent = None):
        QtGui.QTreeView.__init__(self, parent)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setGeometry(500,200, 400, 300)
        self.setUniformRowHeights(False) #optimize: but for word wrap, we don't want this!
        print "uniform heights in tree?", self.uniformRowHeights()

        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Task', 'Description'])
        self.setModel(self.model)

        self.rootItem = self.model.invisibleRootItem()
        item0 = [QtGui.QStandardItem('Sneeze'), QtGui.QStandardItem('You have been blocked up')]
        item00 = [QtGui.QStandardItem('Tickle nose, this is a very long entry. Row should resize.'), QtGui.QStandardItem('Key first step')]
        item1 = [QtGui.QStandardItem('<b>Get a job</b>'), QtGui.QStandardItem('Do not blow it')]
        self.rootItem.appendRow(item0)
        item0[0].appendRow(item00)
        self.rootItem.appendRow(item1)
        self.setColumnWidth(0,150)
        self.expandAll()
        self.setWordWrap(True)

        self.setItemDelegate(ItemWordWrap(self))

class ItemWordWrap(QtGui.QStyledItemDelegate):
    def __init__(self, parent=None):
        QtGui.QStyledItemDelegate.__init__(self, parent)
        self.parent = parent
    def paint(self, painter, option, index):
        text = index.model().data(index)
        document = QtGui.QTextDocument() # #print "dir(document)", dir(document)
        document.setHtml(text)
        document.setTextWidth(option.rect.width())  #keeps text from spilling over into adjacent rect
        painter.save()
        painter.translate(option.rect.x(), option.rect.y())
        document.drawContents(painter)  #draw the document with the painter
        painter.restore()
        index.model().setData(index, option.rect.width(), QtCore.Qt.UserRole + 1)

    def sizeHint(self, option, index):
        #Size should depend on number of lines wrapped
        text = index.model().data(index)
        document = QtGui.QTextDocument()
        document.setHtml(text)
        width = index.model().data(index, QtCore.Qt.UserRole + 1)
        if not width:
            width = 20
        document.setTextWidth(width)
        return QtCore.QSize(document.idealWidth() + 10,  document.size().height())

def main():
    app = QtGui.QApplication(sys.argv)
    myTree = SimpleTree()
    myTree.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()