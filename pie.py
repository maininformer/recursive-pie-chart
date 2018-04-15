from pdb import set_trace as st

def auto_register_with_parent(cls):
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
            old_setattr(self, 'level', value.level+1)
            children = value.children
            for child in children: # redistribute among the children
                __setattr__(child, 'area', value.area/len(children))
        if name == 'area' and old != value:
            if len(self.children) > 0:  # cannot be on the previous line; will break on the first pass of the constructor
                children = self.children
                for child in children:
                    old_setattr(child, 'area', self.area/len(children))

    cls.__setattr__ = __setattr__

    return cls

@auto_register_with_parent
class Slice(object):
    def __init__(self, label='template', parent=None, level=0, area=1.0):
        self.parent = parent
        self.children = []
        self.label = label
        self.level = level
        self.area = area




# draw({'cash':None, 'equity':{'owner':None, 'vc':None}})

def tests():
    def test_children_should_register_themselves_to_parents():
        p=Slice()
        c=Slice()
        c.parent=p
        assert p.children[0] is c

    def test_area_should_redistribute_correctly():
        p=Slice()
        c1=Slice()
        c1.parent=p

        cc1=Slice()
        cc1.parent=c1

        c2=Slice()
        c2.parent=p

        assert c2.area == c1.area == 0.5
        assert cc1.area == 0.5


    test_children_should_register_themselves_to_parents()
    test_area_should_redistribute_correctly()

tests()
