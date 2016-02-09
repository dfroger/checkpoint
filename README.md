# clickle
Store Python Class data members in HDF5 files

## Development 

Create a `Conda` environment:

    conda create -n clash python=3.5 h5py pyyaml

Install `clash` in development mode:

    source activate clash
    pip install -e .

Run tests:

    cd clash/test
    python test_clash.py

## Example

See the file `example/main.py`:

    import numpy as np
    import h5py

    from clash import Dumper, create_loader

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

The file `foo.h5` is created, containing (`h5ls -r foo.h5`):

    /                        Group
    /a                       Dataset {SCALAR}
    /bar                     Group
    /bar/baz                 Group
    /bar/baz/z               Dataset {SCALAR}
    /bar/x                   Dataset {11}
    /bar/y                   Dataset {11}
    /d                       Group
    /d/keys                  Dataset {2, 2}
    /d/values                Dataset {2, 2}
    /l                       Group
    /l/data                  Dataset {9}
    /l/index                 Dataset {6}
