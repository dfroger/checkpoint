import unittest

import numpy as np
import h5py

from clash.test.data import FooArray, FooScalar, FooCRS, \
    FooDict, FooYAML, FooRecurse

def h5tmp():
    """HDF5 file, in memory only: no written to the disk"""
    return h5py.File('tmp.h5', driver='core', backing_store=False)

class TestPersistArray(unittest.TestCase):
    """Test numpy array dump and load"""

    def test_int(self):
        data = np.arange(5)
        foo = FooArray(data)
        with h5tmp() as f:
            foo.dump(f)
            foo_bis = FooArray.load(f)
            np.testing.assert_array_equal(foo_bis.data, foo.data)

class TestPersistScalar(unittest.TestCase):
    """Test numpy array dump and load"""

    def test_int(self):
        data = 5
        foo = FooScalar(data)
        with h5tmp() as f:
            foo.dump(f)
            foo_bis = FooScalar.load(f)
            self.assertEqual(foo_bis.data, foo.data)

class TestPersistCRS(unittest.TestCase):
    """Test crs list dump and load"""

    def check(self, data):
        foo = FooCRS(data)
        with h5tmp() as f:
            foo.dump(f)
            foo_bis = FooCRS.load(f)
            self.assertListEqual(foo_bis.data, foo.data)

    def test_list(self):
        data = [ [1,5,2], [6,0], [], [1,3,4], [7] ]
        self.check(data)

    def test_set(self):
        data = [ {1,5,2}, {6,0}, set(), {1,3,4}, {7} ]
        self.check(data)

    def test_tuple(self):
        data = [ (1,5,2), (6,0), (), (1,3,4), (7,) ]
        self.check(data)

    def test_array(self):
        data = [ np.array([1,5,2]), np.array([6,0]), np.array([]), 
                 np.array([1,3,4]), np.array([7,]) ]

        foo = FooCRS(data)
        with h5tmp() as f:
            foo.dump(f)
            foo_bis = FooCRS.load(f)
            for array1, array2 in zip(foo.data, foo_bis.data):
                np.testing.assert_array_equal(array1, array2)

class TestPersistDict(unittest.TestCase):
    """Test dictionnary dump and load
    
    Note that dumped Python type (int, float) are loaded as Numpy types
    (int64, float32, ...). This should not be a problem with Numpy
    1.9.0 and greater https://github.com/numpy/numpy/issues/2951
    """

    def check(self, data):
        foo = FooDict(data)
        with h5tmp() as f:
            foo.dump(f)
            foo_bis = FooDict.load(f)
            self.assertDictEqual(foo_bis.data, foo.data)

    def test_tuple2list(self):
        data = {(1,2): [10,20], (3,4): [30,40]}
        self.check(data)

    def test_tuple2int(self):
        data = {(1,2): 12, (3,4): 34}
        self.check(data)

    def test_int2list(self):
        data = {12: [1,2], 34: [3,4]}
        self.check(data)

    def test_npint2list(self):
        a,b = np.array( [12, 34] )
        data = {a: [1,2], b: [3,4]}
        self.check(data)

    def test_int2array(self):
        data = {12: np.array([1,2]), 34: np.array([3,4])}

        foo = FooDict(data)
        with h5tmp() as f:
            foo.dump(f)
            foo_bis = FooDict.load(f)
            for array1, array2 in zip(foo.data.values(), foo_bis.data.values()):
                np.testing.assert_array_equal(array1, array2)

class TestPersistYAML(unittest.TestCase):
    """Test numpy array dump and load"""

    def test_dict(self):
        data = {1:'one', 'two': 2, 'tree': [1,2,'three']}
        foo = FooYAML(data)
        with h5tmp() as f:
            foo.dump(f)
            foo_bis = FooYAML.load(f)
            self.assertDictEqual(foo.data, foo_bis.data)

class TestPersistRecurse(unittest.TestCase):
    """Test recursive dump and load"""

    def test_foo_foo(self):

        foo_array = FooScalar(5)
        foo_recurse = FooRecurse(foo_array)

        with h5tmp() as f:
            foo_recurse.dump(f)
            foo_recurse_bis = FooRecurse.load(f)

        self.assertEqual(foo_recurse_bis.data.data, foo_recurse.data.data)

if __name__ == '__main__':
    unittest.main()
