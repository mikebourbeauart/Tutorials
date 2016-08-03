# simple tree builder.

# (node, parent, title)
els = (
 ('a', 'type', 'id', 0),
 ('b', 'type', 'id', 1),
 ('c', 'type', 'id', 1),
 ('d', 'type', 'id', 0),
 ('e', 'type', 'id', 4),
 ('f', 'type', 'id', 5),
 ('g', 'type', 'id', 5),
)

class Node:
 def __init__(self, nodeName, nodeType, nodeId, nodeParent):
     self.nodeName = nodeName
     self.nodeType = nodeType
     self.nodeId = nodeId
     self.nodeParent = nodeParent
     self.children = []

treeMap = {}
Root = Node("Root", 'Root','Root',0)
treeMap[Root.nodeId] = Root

for element in els:
    nodeName, nodeType, nodeId, nodeParent = element
    treeMap[nodeParent] = Node(nodeName,nodeType, nodeId, nodeParent )


    if not nodeParent in treeMap:
        treeMap[nodeParent] = Node(0, '')
    treeMap[nodeParent].children.append(treeMap[nodeParent])

def print_map(node, lvl=0):
    for n in node.children:
        print '    ' * lvl + n.title
        if len(n.children) > 0:
            print_map(n, lvl+1)
print treeMap
print_map(Root)

"""
Output:
a
    b
    c
d
    e
        f
    g
"""