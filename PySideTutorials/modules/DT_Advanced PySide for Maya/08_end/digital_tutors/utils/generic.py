import maya.cmds as mc

#------------------------------------------------------------------------------#

def undo(func):
    def wrapper(*args, **kwargs):
        mc.undoInfo(openChunk=True)
        try:
            ret = func(*args, **kwargs)
        finally:
            mc.undoInfo(closeChunk=True)
        return ret
    return wrapper

#------------------------------------------------------------------------------#
