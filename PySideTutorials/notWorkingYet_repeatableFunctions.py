import maya.cmds as cmds

_repeat_command_str = 'python("{0}._repeat_command()")'.format( __name__ )
 
_repeat_function = None
_args = None
_kwargs = None
 
def _repeat_command():
    if _repeat_function is not None:
        _repeat_function(*_args, **_kwargs)
 
def repeatable(function):
    def wrapper(*args, **kwargs):
        global _repeat_function
        global _args
        global _kwargs
 
        _repeat_function = function
        _args = args
        _kwargs = kwargs
 
        ret = function(*args, **kwargs)
 
        try:
            cmds.repeatLast(ac=_repeat_command_str, acl=function.__name__)
        except RuntimeError:
            pass 
 
        return ret
    return wrapper
 
@repeatable
def example():
    print "example()"
    