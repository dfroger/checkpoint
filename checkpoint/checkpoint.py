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

class ErrorManager:

    def __call__(self, err, filename, name, actual, expected, store_as):
        raise AssertionError(err)

_is_active = False
_mode = None
_expected_dir = None
_actual_dir = '.'
_excluded = None
_record = []
_simutime = None
_relative_tolerance = 1e-07
_absolute_tolerance = 0.
_filenamer = lambda label : label + '.h5'
_error_manager = ErrorManager()

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

def activate_checkpoints(expected_dir, actual_dir, mode, excluded=[],
                         verbose=False):
    global _is_active, _mode, _expected_dir, _excluded
    _is_active = True
    _mode = mode
    _expected_dir = expected_dir
    _actual_dir = actual_dir
    _excluded = excluded
    if verbose:
        print("checkpoint: directory of expected data is:", expected_dir)
        print("checkpoint: directory of actual data is:", actual_dir)

def _is_excluded(label, name):
    checkpoint_name = label + '.' + name
    for name in subnames(checkpoint_name):
        if name in _excluded:
            return True
    return False

class CheckPoint:

    def __init__(self, label, from_object=None, from_dict=None):
        self.label = label
        self.filename = _filenamer(label)
        self.from_object = from_object
        self.from_dict = from_dict
    
    def __enter__(self):
        if not _is_active:
            return self
        expected_fp = Path(_expected_dir) / self.filename
        if _mode == 'w':
            self.expected_f = h5py.File(str(expected_fp), 'w')
            self.expected_writer = Writer(self.expected_f,
                                          from_object = self.from_object,
                                          from_dict = self.from_dict)
        elif _mode == 'r':
            self.expected_f = h5py.File(str(expected_fp), 'r')
            self.expected_reader = Reader(self.expected_f)

            actual_fp = Path(_actual_dir) / self.filename
        else:
            raise ValueError("No such mode: {!r}".format(_mode))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not _is_active:
            return
        if _mode == 'w':
            self.expected_f.close()
        elif _mode == 'r':
            self.expected_f.close()

    def __call__(self, name, data=None, store_as='array'):
        if not self.is_active(name):
            return
        _record.append((self.filename, name))
        if _mode == 'w':
            self.expected_writer(name, data=data, store_as=store_as)
        elif _mode == 'r':
            expected = self.expected_reader(name, store_as=store_as)
            if data is not None:
                actual = data
            elif self.from_object is not None:
                actual = getattr(self.from_object, name)
            elif self.from_dict is not None:
                actual = self.from_dict[name]
            else:
                raise ValueError("No actual data.")
            try:
                self.check_data(actual, expected, store_as)
            except AssertionError as err:
                _error_manager(err, self.filename, name, actual, expected,
                               store_as)
        else:
            raise ValueError("No such mode: {!r}".format(_mode))

    def check_data(self, actual, expected, store_as):
        if store_as == 'array':
            if len(expected.shape) == len(actual.shape) + 1:
                expected= expected[0,...]      
            np.testing.assert_allclose(actual, expected,
                                       rtol=_relative_tolerance,
                                       atol=_absolute_tolerance)
        elif store_as == 'scalar':
            assert  math.isclose(actual, expected,
                                 rel_tol=_relative_tolerance,
                                 abs_tol=_absolute_tolerance)
        else:
            assert actual == expected

    def is_active(self, name):
        return _is_active and not _is_excluded(self.label, name)

def report():
    for filepath, name in _record:
        print('checkoint: {}: {}'
            .format(filepath, name))

def reset():
    global _is_active, _simutime, _excluded, _expected_dir, _mode, _record
    _is_active = False
    _simutime = None
    _mode = None
    _excluded = None
    _expected_dir = '.'
    _record = []

def configure(rtol, atol):
    global _absolute_tolerance, _relative_tolerance
    _relative_tolerance = rtol
    _absolute_tolerance = atol

if __name__ == '__main__':
    doctest.testmod()
