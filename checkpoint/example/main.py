import numpy as np
import h5py

from checkpoint import Dumper, create_loader

class Baz:

    def __init__(self):
        self.z = {1:'one', 'two': 2, 'tree': [1,2,'three']}

    def dump(self, group):
        dumper = Dumper(group, self)
        dumper.yaml('z')

    @staticmethod
    def load(group):
        foo, loader = create_loader(Baz, group)
        loader.yaml('z')
        return foo

class Bar:

    def __init__(self):
        self.x = np.linspace(0,5,11)
        self.y = np.linspace(0,1,11)
        self.baz = Baz()

    def dump(self, group):
        dumper = Dumper(group, self)
        dumper.arrays('x', 'y')
        dumper.recurse('baz')

    @staticmethod
    def load(group):
        foo, loader = create_loader(Bar, group)
        loader.arrays('x', 'y')
        loader.recurse(Baz, 'baz')
        return foo

class Foo:

    def __init__(self):
        self.a = 1.1
        self.l = [ [1,5,2], [6,0], [], [1,3,4], [7] ]
        self.d = {(1,2): [10,20], (3,4): [30,40]}
        self.bar = Bar()

    def dump(self, group):
        dumper = Dumper(group, self)
        dumper.scalar('a')
        dumper.crs('l')
        dumper.dict('d')
        dumper.recurse('bar')

    @staticmethod
    def load(group):
        foo, loader = create_loader(Foo, group)
        loader.scalar('a')
        loader.crs('l')
        loader.dict('d')
        loader.recurse(Bar, 'bar')
        return foo

def main():
    foo = Foo()

    with h5py.File('foo.h5', 'w') as f:
        foo.dump(f)

    with h5py.File('foo.h5', 'r') as f:
        foo_bis = Foo.load(f)

    assert foo_bis.a == foo.a
    assert foo_bis.l == foo.l
    assert foo_bis.d == foo.d
    np.testing.assert_array_equal(foo_bis.bar.x, foo.bar.x)
    np.testing.assert_array_equal(foo_bis.bar.y, foo.bar.y)
    assert foo_bis.bar.baz.z == foo.bar.baz.z

if __name__ == '__main__':
    main()
