from collections import OrderedDict

import yaml
import numpy as np

def list_to_crs(list_of_items):
    """
    >>> list_of_items = [ [1,5,2], [6,0], [], [1,3,4], [7] ]
    >>> data, index = list_to_crs(list_of_items)
    >>> print(data)
    [1 5 2 6 0 1 3 4 7]
    >>> print(index)
    [0 3 5 5 8 9]
    """
    data = []
    index = [0, ]
    length = 0
    for items in list_of_items:
        data.extend(items)
        length += len(items)
        index.append(length)
    data = np.array(data)
    index = np.array(index)
    return data, index

def need_conversion(obj_type):
    return obj_type in [tuple, list, set, frozenset]

def set_iterable_converter(h5obj, obj_type):
    if need_conversion(obj_type):
        h5obj.attrs['iterable'] = obj_type.__name__

def write_crs(group, name, list_of_items):
    data, index = list_to_crs(list_of_items)
    subgroup = group.create_group(name)
    subgroup.create_dataset('data', data=data)
    subgroup.create_dataset('index', data=index)
    items = list_of_items[0]
    items_type = type(items)
    set_iterable_converter(subgroup, items_type)

class Writer:

    def __init__(self, group, from_object=None, from_dict=None):
        self.group = group
        self.from_object = from_object
        self.from_dict = from_dict

    def __call__(self, name, store_as='array'):
        if store_as == 'array':
            self.array(name)
        elif store_as == 'scalar':
            self.scalar(name)
        elif store_as == 'crs':
            self.crs(name)
        elif store_as == 'dict':
            self.dict(name)
        elif store_as == 'dict_crs':
            self.dict_crs(name)
        elif store_as == 'yaml':
            self.yaml(name)
        else:
            raise ValueError("No such type: %r" % (store_as,))

    def array(self, name, data=None):
        a = self._get(name, data)
        self.group.create_dataset(name, data=a)

    def arrays(self, *names):
        assert self.from_object is not None or self.from_dict is not None
        for name in names:
            self.array(name)

    def scalar(self, name, data=None):
        s = self._get(name, data)
        self.group.create_dataset(name, data=s)

    def crs(self, name, data=None):
        list_of_items = self._get(name, data)
        write_crs(self.group, name, list_of_items)

    def dict(self, name, data=None):
        d = self._get(name, data)
        subgroup = self.group.create_group(name)
        self._write_obj_list('keys', subgroup, list(d.keys()))
        self._write_obj_list('values', subgroup, list(d.values()))
        if isinstance(d, OrderedDict):
            subgroup.create_dataset('ordered', data=1)
        else:
            subgroup.create_dataset('ordered', data=0)

    def dict_crs(self, name, data=None):
        d = self._get(name, data)
        subgroup = self.group.create_group(name)
        self._write_obj_list('keys', subgroup, list(d.keys()))
        write_crs(subgroup, "values", list(d.values()))
        if isinstance(d, OrderedDict):
            subgroup.create_dataset('ordered', data=1)
        else:
            subgroup.create_dataset('ordered', data=0)

    def yaml(self, name, data=None):
        obj = self._get(name, data)
        data = yaml.dump(obj)
        dset = self.group.create_dataset(name, data=data)
        dset.attrs['format'] = 'yaml'

    def _write_obj_list(self, name, group, obj_list):
        obj = obj_list[0]
        obj_type = type(obj)
        if need_conversion(obj_type):
            dset = group.create_dataset(name, data=[list(obj) for obj in obj_list])
            set_iterable_converter(dset, obj_type)
        else:
            dset = group.create_dataset(name, data=obj_list)

    def _get(self, name, data):
        if data is not None:
            return data
        elif self.from_object is not None:
            return getattr(self.from_object, name)
        elif self.from_dict is not None:
            return self.from_dict[name]
        else:
            raise ValueError("No data to write.")

if __name__ == '__main__':
    doctest.testmod()
