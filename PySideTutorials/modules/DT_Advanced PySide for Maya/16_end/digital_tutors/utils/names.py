import maya.cmds as mc
from ..utils.generic import undo

#------------------------------------------------------------------------------#

def getAlpha(value, capital=False):
    ''' Convert an integer value to a character. a-z then double, aa-zz etc. '''

    # calculate number of characters required
    #
    base_power = base_start = base_end = 0
    while value >= base_end:
        base_power += 1
        base_start = base_end
        base_end += pow(26, base_power)
    base_index = value - base_start

    # create alpha representation
    #
    alphas = ['a'] * base_power
    for index in range(base_power - 1, -1, -1):
        alphas[index] = chr(97 +  (base_index % 26))
        base_index /= 26

    if capital: return ''.join(alphas).upper()
    return ''.join(alphas)

#------------------------------------------------------------------------------#

class RenameException(Exception):
    def __init__(self, nodes):
        if not hasattr(nodes, '__iter__'):
            nodes = [nodes]
        error_msg = "Failed to rename one of more nodes.\n"

        for node in nodes:
            if not mc.objExists(node):
                error_msg += "\t'%s' no longer exists.\n" %node

            elif mc.lockNode(node, q=True, l=True):
                error_msg += "\t'%s' is locked.\n" %node

            else:
                error_msg += "\t'%s' failure unknown.\n" %node

        Exception.__init__(self, error_msg)

@undo
def rename(nodes, text,
           prefix  = None,
           suffix  = None,
           padding = 0,
           letters = False,
           capital = False):

    if prefix:
        text = '%s_%s' %(prefix, text)

    # if single node, try without letter or number
    #
    if len(nodes) == 1:
        node = nodes[0]

        new_name = text
        if suffix:
            new_name += suffix

        if node == new_name:
            return new_name

        failed_nodes = []
        if not mc.objExists(new_name):
            try:
                mc.rename(node, new_name)
            except RuntimeError:
                raise RenameException(node)
            return new_name

    # rename nodes to tmp
    #
    new_node_names = []; failed_nodes = []
    for node in nodes:
        try:
            new_node_names.append(mc.rename(node, '__tmp__'))
        except RuntimeError:
            failed_nodes.append(node)

    # get new names
    #
    new_nodes = []
    for node_name in new_node_names:
        new_name = _findAvaliableName(text,    suffix,  1,
                                      padding, letters, capital)
        try:
            new_nodes.append(mc.rename(node_name, new_name))
        except RuntimeError:
            failed_nodes.append(node)

    if failed_nodes:
        raise RenameException(failed_nodes)

    return new_nodes


def _findAvaliableName(name,  suffix,
                       index, padding,
                       letters = False,
                       capital = False):
    ''' Recursively find a free name matching specified criteria. '''

    test_name = name

    if letters is True:
        letter    = getAlpha(index - 1, capital)
        test_name = '%s_%s' %(name, letter)
    else:
        test_name = '%s_%s' %(name, str(index).zfill(padding))

    if suffix:
        test_name = '%s_%s' %(test_name, suffix)

    # if object exists, try next index
    #
    if mc.objExists(test_name):
        return _findAvaliableName(name,    suffix,  index + 1,
                                  padding, letters, capital)

    return test_name

#------------------------------------------------------------------------------#

@undo
def find_replace(nodes, find_text, replace_text):
    shapes    = mc.ls(nodes, s=True)
    shape_set = set(shapes)

    new_nodes_names = []; failed_nodes = []
    for node in nodes:
        if not find_text in node: continue
        if node in shape_set:     continue

        try:
            new_nodes_names.append((node, mc.rename(node, '__tmp__')))
        except RuntimeError:
            failed_nodes.append(node)

    for shape in shapes:
        if not find_text in shape: continue
        if not mc.objExists(shape):
            try:
                new_name = mc.rename(shape, shape.replace(find_text, '__tmp__'))
                new_nodes_names.append((shape, new_name))
            except RuntimeError:
                failed_nodes.append(node)

    new_names = []
    for name, new_node in new_nodes_names:
        new_name = name.replace(find_text, replace_text)
        new_names.append(mc.rename(new_node, new_name))

    return new_names

#------------------------------------------------------------------------------#
