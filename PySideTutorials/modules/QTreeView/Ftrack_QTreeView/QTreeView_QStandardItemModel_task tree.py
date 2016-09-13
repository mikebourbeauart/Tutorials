'''orig site: http://rowinggolfer.blogspot.com/2010/05/qtreeview-and-qabractitemmodel-example.html'''

import os
import sys

os.environ['FTRACK_SERVER'] = 'https://firstborn.ftrackapp.com'
os.environ['FTRACK_API_USER'] = 'Mike'
os.environ['FTRACK_API_KEY'] = 'd545801e-9076-4b38-a748-e7b2fa7be162'
#.environ['FTRACK_EVENT_PLUGIN_PATH'] = ('S:\_Studio\_ASSETS\Tutorials\Ftrack\NewFtrackPipeline\code\ftrack_plugins')

# MB Pipeline
mbp_dir_init = os.path.abspath(os.path.dirname( __file__ ) )
mbp_dir = mbp_dir_init.rpartition('mb_Pipeline')[0] + 'mb_Pipeline'
mbp_python_dir = '{0}/code/python'.format( mbp_dir )

if not mbp_python_dir in sys.path:
    sys.path.append( mbp_python_dir )

import ftrack_api
from PySide import QtGui, QtCore

# simple tree builder.

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

def print_map(node, lvl=0):
 for n in node.children:
     print '    ' * lvl + n.title
     if len(n.children) > 0:
         print_map(n, lvl+1)

print_map(Root)


