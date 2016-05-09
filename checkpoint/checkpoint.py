"""
This module make use of global variables, in the same flavor of the logging
module does.
"""

import doctest
import math
from pathlib import Path

import numpy as np
import h5py
from . import Writer, Reader

_is_active = False
_mode = None
_output_dir = '.'
_excluded = None
_record = []
_simutime = None
_relative_tolerance = 1e-07
_absolute_tolerance = 0.
_filenamer = lambda label : label + '.h5'

def subnames(fullname):
    """
    Iterate over module-like sub-names.
    >>> for name in subnames('x.y.z'):
    ...     print('<' + name + '>')
    <x.y.z>
    <x.y>
    <x>
    <>
    """
    parts = fullname.split('.')
    for n in range(len(parts),-1,-1):
        yield '.'.join(parts[:n])

def activate_checkpoints(output_dir, mode, excluded=[]):
    global _is_active, _mode, _output_dir, _excluded
    _is_active = True
    _mode = mode
    _output_dir = output_dir
    _excluded = excluded

def _is_excluded(label, attr_name):
    checkpoint_name = label + '.' + attr_name
    for name in subnames(checkpoint_name):
        if name in _excluded:
            return True
    return False

class CheckPoint:

    def __init__(self, label, from_object=None, from_dict=None):
        self.label = label
        self.from_object = from_object
        self.from_dict = from_dict
    
    def __enter__(self):
        if not _is_active:
            return self
        filename = _filenamer(self.label)
        self.filepath = Path(_output_dir) / filename
        if _mode == 'w':
            self.f = h5py.File(str(self.filepath), 'w')
            self.writer = Writer(self.f,
                                 from_object = self.from_object,
                                 from_dict = self.from_dict)
        elif _mode == 'r':
            self.f = h5py.File(str(self.filepath), 'r')
            self.reader = Reader(self.f)
        else:
            raise ValueError("No such mode: {!r}".format(_mode))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not _is_active:
            return
        self.f.close()

    def __call__(self, attr_name, data=None, store_as='array'):
        if not self.is_active(attr_name):
            return
        if _mode == 'w':
            self.writer(attr_name, data=data, store_as=store_as)
        elif _mode == 'r':
            expected = self.reader(attr_name, store_as=store_as)
            if data is not None:
                actual = data
            elif self.from_object is not None:
                actual = getattr(self.from_object, name)
            elif self.from_dict is not None:
                actual = self.from_dict[name]
            else:
                raise ValueError("No actual data.")
            self.check_data(actual, expected, store_as)
        else:
            raise ValueError("No such mode: {!r}".format(_mode))
        _record.append((self.filepath, attr_name))

    def check_data(self, actual, expected, store_as):
        if store_as == 'array':
            np.testing.assert_allclose(actual, expected,
                                       rtol=_relative_tolerance,
                                       atol=_absolute_tolerance)
        elif store_as == 'scalar':
            assert  math.isclose(actual, expected,
                                 rel_tol=_relative_tolerance,
                                 abs_tol=_absolute_tolerance)
        else:
            assert actual == expected

    def is_active(self, attr_name):
        return _is_active and not _is_excluded(self.label, attr_name)

def report():
    for filepath, attr_name in _record:
        print('checkoint: {}: {}'
            .format(filepath, attr_name))

def reset():
    global _is_active, _simutime, _excluded, _output_dir, _mode, _record
    _is_active = False
    _simutime = None
    _mode = None
    _excluded = None
    _output_dir = '.'
    _record = []

def configure(rtol, atol):
    global _absolute_tolerance, _relative_tolerance
    _relative_tolerance = rtol
    _absolute_tolerance = atol

if __name__ == '__main__':
    doctest.testmod()
