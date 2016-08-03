import sys
from PySide.QtGui import *


class TreeTime(QMainWindow):
    def __init__(self):
        super(TreeTime, self).__init__()
        self.initUI()

    def initUI(self):
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.statusBar()

        self.make_tree()

        self.show()

    def make_tree(self):
        # init widgets
        self.tgb = QGroupBox("[Tree Group Box Title]")
        self.main_layout.addWidget(self.tgb)

        tgb_layout = QVBoxLayout()
        self.tgb.setLayout(tgb_layout)

        view = QTreeView()
        tgb_layout.addWidget(view)

        debug_btn = QPushButton("DEBUG")
        tgb_layout.addWidget(debug_btn)

        # view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        view.setSelectionBehavior(QAbstractItemView.SelectRows)
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['col1', 'col2', 'col3'])
        view.setModel(model)
        view.setUniformRowHeights(True)

        # populate data
        for i in range(10):
            parent1 = QStandardItem('Family {}. Some long status text for sp'.format(i))
            for j in range(3):
                child1 = QStandardItem('Child {}'.format(i*3+j))
                child2 = QStandardItem('row: {}, col: {}'.format(i, j+1))
                child3 = QStandardItem('row: {}, col: {}'.format(i, j+2))
                parent1.appendRow([child1, child2, child3])
            model.appendRow(parent1)
            # span container columns
            view.setFirstColumnSpanned(i, view.rootIndex(), True)

        # expand third container
        index = model.indexFromItem(parent1)
        view.expand(index)

        # select last row
        selmod = view.selectionModel()
        index2 = model.indexFromItem(child3)
        selmod.select(index2, QItemSelectionModel.Select|QItemSelectionModel.Rows)

        def print_debug_info():
            print('')
            for child in view.children():
                print("child "+repr(child)) #not sure what all these are yet
            print('')
            print('self.main_widget.frameSize: '+repr(self.main_widget.frameSize()))
            print('view.parent().parent().frameSize(): '+repr(view.parent().parent().frameSize())) #group box
            # print('self.frameSize: '+repr(self.frameSize()))
            print('self.tgb.frameSize: '+repr(self.tgb.frameSize()))
            print('view.parent(): '+repr(view.parent()))
            print('view.parent().frameSize(): '+repr(view.parent().frameSize()))
            # print('view.parent().frameSize(): '+repr(view.parent().frameSize())+" (before)")
            # print('view.parent().adjustSize(): '+repr(view.parent().adjustSize()))
            # print('view.parent().frameSize(): '+repr(view.parent().frameSize())+" (after)")
            print('view.viewport(): '+repr(view.viewport()))
            print('view.viewport().frameSize(): '+repr(view.viewport().frameSize()))
            # print('view.parent().parent().parent().frameSize(): '+repr(view.parent().parent().parent().frameSize()))
            # print('calling setViewport: '+repr(view.setViewport(QWidget())))
            # view.adjustSize()

        debug_btn.clicked.connect(print_debug_info)

    def sayHello(self):
        self.statusBar().showMessage("Hello World!")
        import time; time.sleep(2)
        self.statusBar().showMessage("")

    def sayWords(self, words):
        self.statusBar().showMessage(words)


if __name__ == '__main__':
    app = QApplication([])
    tt = TreeTime()
    sys.exit(app.exec_())