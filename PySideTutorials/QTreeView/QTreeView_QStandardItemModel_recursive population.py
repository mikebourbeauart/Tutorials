from PySide.QtGui import *
import sys
import types

class MainFrame(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        tree = {'root': {
                    "1": ["A", "B", "C"],
                    "2": {
                        "2-1": ["G", "H", "I"],
                        "2-2": ["J", "K", "L"]},
                    "3": ["D", "E", "F"]}
        }

        # (node, parent, title)
        els = (
            (1, 0, 'a'),
            (2, 1, 'b'),
            (3, 1, 'c'),
            (4, 0, 'd'),
            (5, 4, 'e'),
            (6, 5, 'f'),
            (7, 4, 'g')
        )

        class Node:
            def __init__(self, n, s):
                self.id = n
                self.title = s
                self.children = []

        treeMap = {}
        Root = Node(0, "Root")
        treeMap[Root.id] = Root
        for element in els:
            nodeId, parentId, title = element
            if not nodeId in treeMap:
                treeMap[nodeId] = Node(nodeId, title)
            else:
                treeMap[nodeId].id = nodeId
                treeMap[nodeId].title = title

            if not parentId in treeMap:
                treeMap[parentId] = Node(0, '')
            treeMap[parentId].children.append(treeMap[nodeId])

        print treeMap

        self.tree = QTreeView(self)
        layout = QHBoxLayout(self)
        layout.addWidget(self.tree)

        root_model = QStandardItemModel()
        self.tree.setModel(root_model)
        self._populateTree(treeMap, root_model.invisibleRootItem())

    def _populateTree(self, children, parent):
        for child in sorted(children):
            child_item = QStandardItem(child)
            parent.appendRow(child_item)
            if isinstance(children, types.DictType):
                self._populateTree(children[child], child_item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainFrame()
    main.show()
    sys.exit(app.exec_())