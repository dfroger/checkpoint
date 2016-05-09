import numpy as np
import h5py

from checkpoint import Writer, create_reader

class Baz:

    def __init__(self):
        self.z = {1:'one', 'two': 2, 'tree': [1,2,'three']}

    def write(self, group):
        writer = Writer(group, self)
        writer.yaml('z')

    @staticmethod
    def read(group):
        foo, reader = create_reader(Baz, group)
        reader.yaml('z')
        return foo

class Bar:

    def __init__(self):
        self.x = np.linspace(0,5,11)
        self.y = np.linspace(0,1,11)
        self.baz = Baz()

    def write(self, group):
        writer = Writer(group, self)
        writer.arrays('x', 'y')
        writer.recurse('baz')

    @staticmethod
    def read(group):
        foo, reader = create_reader(Bar, group)
        reader.arrays('x', 'y')
        reader.recurse(Baz, 'baz')
        return foo

class Foo:

    def __init__(self):
        self.a = 1.1
        self.l = [ [1,5,2], [6,0], [], [1,3,4], [7] ]
        self.d = {(1,2): [10,20], (3,4): [30,40]}
        self.bar = Bar()

    def write(self, group):
        writer = Writer(group, self)
        writer.scalar('a')
        writer.crs('l')
        writer.dict('d')
        writer.recurse('bar')

    @staticmethod
    def read(group):
        foo, reader = create_reader(Foo, group)
        reader.scalar('a')
        reader.crs('l')
        reader.dict('d')
        reader.recurse(Bar, 'bar')
        return foo

def main():
    foo = Foo()

    with h5py.File('foo.h5', 'w') as f:
        foo.write(f)

    with h5py.File('foo.h5', 'r') as f:
        foo_bis = Foo.read(f)

    assert foo_bis.a == foo.a
    assert foo_bis.l == foo.l
    assert foo_bis.d == foo.d
    np.testing.assert_array_equal(foo_bis.bar.x, foo.bar.x)
    np.testing.assert_array_equal(foo_bis.bar.y, foo.bar.y)
    assert foo_bis.bar.baz.z == foo.bar.baz.z

if __name__ == '__main__':
    main()
