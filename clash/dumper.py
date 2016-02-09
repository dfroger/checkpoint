import collections

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

class Dumper:

    def __init__(self, group, dumped_instance, dump_method='dump'):
        self.group = group
        self.dumped_instance = dumped_instance
        self.dump_method = dump_method

    def array(self, name):
        a = getattr(self.dumped_instance, name)
        self.group.create_dataset(name, data=a)

    def arrays(self, *names):
        for name in names:
            self.array(name)

    def scalar(self, name):
        s = getattr(self.dumped_instance, name)
        self.group.create_dataset(name, data=s)

    def crs(self, name):
        list_of_items = getattr(self.dumped_instance, name)
        data, index = list_to_crs(list_of_items)
        subgroup = self.group.create_group(name)
        subgroup.create_dataset('data', data=data)
        subgroup.create_dataset('index', data=index)
        items = list_of_items[0]
        items_type = type(items)
        if items_type in [tuple, list, set]:
            subgroup.attrs['iterable'] = items_type.__name__

    def dict(self, name):
        d = getattr(self.dumped_instance, name)
        subgroup = self.group.create_group(name)
        self._dump_obj_list('keys', subgroup, list(d.keys()))
        self._dump_obj_list('values', subgroup, list(d.values()))

    def yaml(self, name):
        obj = getattr(self.dumped_instance, name)
        data = yaml.dump(obj)
        dset = self.group.create_dataset(name, data=data)
        dset.attrs['format'] = 'yaml'

    def recurse(self, name):
        obj = getattr(self.dumped_instance, name)
        obj.dump( self.group.create_group(name) )

    def _dump_obj_list(self, name, group, obj_list):
        dset = group.create_dataset(name, data=obj_list)
        obj = obj_list[0]
        obj_type = type(obj)
        if obj_type in [tuple, list, set]:
            dset.attrs['iterable'] = obj_type.__name__

if __name__ == '__main__':
    doctest.testmod()
