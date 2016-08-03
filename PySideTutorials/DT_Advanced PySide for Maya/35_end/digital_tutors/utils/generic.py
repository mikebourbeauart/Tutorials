import maya.cmds as mc
import pymel.core as pm

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


def undo_pm(func):
    def wrapper(*args, **kwargs):
        pm.undoInfo(openChunk=True)
        try:
            ret = func(*args, **kwargs)
        finally:
            pm.undoInfo(closeChunk=True)
        return ret
    return wrapper

#------------------------------------------------------------------------------#
