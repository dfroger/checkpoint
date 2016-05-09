import unittest

import numpy as np
import h5py

from checkpoint import Reader, Writer

def h5tmp():
    """HDF5 file, in memory only: no written to the disk"""
    return h5py.File('tmp.h5', driver='core', backing_store=False)

class Foo:
    def __init__(self, data):
        self.data = data

class Bar:
    def __init(self):
        self.data = None

class TestArray(unittest.TestCase):
    """Test numpy array write and read"""

    def test_int(self):
        data = np.arange(5)
        foo = Foo(data)
        bar = Bar()
        with h5tmp() as f:
            writer = Writer(f, from_object=foo)
            writer.array('data')
            reader = Reader(f, to_object=bar)
            reader.array('data')
        np.testing.assert_array_equal(foo.data, bar.data)

class TestScalar(unittest.TestCase):
    """Test scalar write and read"""

    def test_int(self):
        data = 5
        foo = Foo(data)
        bar = Bar()
        with h5tmp() as f:
            writer = Writer(f, from_object=foo)
            writer.scalar('data')
            reader = Reader(f, to_object=bar)
            reader.scalar('data')
            self.assertEqual(foo.data, bar.data)

class TestCRS(unittest.TestCase):
    """Test crs list write and read"""

    def check(self, data):
        foo = Foo(data)
        bar = Bar()
        with h5tmp() as f:
            writer = Writer(f, from_object=foo)
            writer.crs('data')
            reader = Reader(f, to_object=bar)
            reader.crs('data')
            self.assertListEqual(foo.data, bar.data)

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

        foo = Foo(data)
        bar = Bar()
        with h5tmp() as f:
            writer = Writer(f, from_object=foo)
            writer.crs('data')
            reader = Reader(f, to_object=bar)
            reader.crs('data')
            np.testing.assert_array_equal(foo.data[0], bar.data[0])
            np.testing.assert_array_equal(foo.data[1], bar.data[1])
            np.testing.assert_array_equal(foo.data[2], bar.data[2])
            np.testing.assert_array_equal(foo.data[3], bar.data[3])
            np.testing.assert_array_equal(foo.data[4], bar.data[4])

class TestDict(unittest.TestCase):
    """Test dictionnary write and read
    
    Note that write Python type (int, float) are loaded as Numpy types
    (int64, float32, ...). This should not be a problem with Numpy
    1.9.0 and greater https://github.com/numpy/numpy/issues/2951
    """

    def check(self, data):
        foo = Foo(data)
        bar = Bar()
        with h5tmp() as f:
            writer = Writer(f, from_object=foo)
            writer.dict('data')
            reader = Reader(f, to_object=bar)
            reader.dict('data')
            self.assertDictEqual(foo.data, bar.data)

    def test_tuple2list(self):
        data = {(1,2): [10,20], (3,4): [30,40]}
        self.check(data)

    def test_tuple2int(self):
        data = {(1,2): 12, (3,4): 34}
        self.check(data)

    def test_int2list(self):
        data = {12: [1,2], 34: [3,4]}
        self.check(data)

    def test_frozenset2list(self):
        data = { frozenset((1,2)): [10,20],
                 frozenset((3,4)): [30,40], }
        self.check(data)

    def test_npint2list(self):
        a,b = np.array( [12, 34] )
        data = {a: [1,2], b: [3,4]}
        self.check(data)

    def test_int2array(self):
        data = {12: np.array([1,2]), 34: np.array([3,4])}

        foo = Foo(data)
        bar = Bar()
        with h5tmp() as f:
            writer = Writer(f, from_object=foo)
            writer.dict('data')
            reader = Reader(f, to_object=bar)
            reader.dict('data')
            np.testing.assert_array_equal(foo.data[12], bar.data[12])
            np.testing.assert_array_equal(foo.data[34], bar.data[34])

class TestDictCRS(unittest.TestCase):
    """Test crs list write and read"""

    def check(self, data):
        foo = Foo(data)
        bar = Bar()
        with h5tmp() as f:
            writer = Writer(f, from_object=foo)
            writer.dict_crs('data')
            reader = Reader(f, to_object=bar)
            reader.dict_crs('data')
            self.assertDictEqual(foo.data, bar.data)

    def test_list(self):
        data = {
            (0,1): [1,5,2],
            (2,3): [6,0],
            (4,5): [],
            (6,7): [1,3,4],
            (8,9): [7],
        }
        self.check(data)

class TestYAML(unittest.TestCase):
    """Test numpy array write and read"""

    def test_dict(self):
        data = {1:'one', 'two': 2, 'tree': [1,2,'three']}
        foo = Foo(data)
        bar = Bar()
        with h5tmp() as f:
            writer = Writer(f, from_object=foo)
            writer.yaml('data')
            reader = Reader(f, to_object=bar)
            reader.yaml('data')
            self.assertDictEqual(foo.data, bar.data)

if __name__ == '__main__':
    unittest.main()
