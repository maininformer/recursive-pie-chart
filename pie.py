from pdb import set_trace as st

def good_parenting(cls):
    _sentinel = object()
    # save the old set attribute method
    old_setattr = getattr(cls, '__setattr__', None)
    def __setattr__(self, name, value):
        # get the old value and update the parents children
        old = getattr(self, name, _sentinel)
        # set the attribute
        old_setattr(self, name, value)
        if name == 'parent' and old !=value and type(value) is Slice:
            value.children.append(self)
    cls.__setattr__ = __setattr__
    return cls

@good_parenting
class Slice(object):
    def __init__(self, label='template', parent=None):
        self.parent = parent
        self.label = label
        self.children = []




# draw({'cash':None, 'equity':{'owner':None, 'vc':None}})

