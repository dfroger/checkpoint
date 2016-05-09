from collections import OrderedDict

import yaml
import numpy as np

def create_reader(ReadClass, group):
    read_instance = ReadClass.__new__(ReadClass)
    reader = Reader(group, read_instance)
    return read_instance, reader
    
def crs_to_list(data, index, items_container=list):
    """
    >>> data = np.array([1, 5, 2, 6, 0, 1, 3,  4, 7])
    >>> index = np.array([0, 3, 5, 5, 8, 9])
    >>> list_of_items = crs_to_list(data, index)
    >>> print(list_of_items)
    [[1, 5, 2], [6, 0], [], [1, 3, 4], [7]]
    """
    list_of_items = []
    nitems = len(index) - 1
    for item in range(nitems):
        i0 = index[item]
        i1 = index[item+1]
        items = items_container(data[i0:i1])
        list_of_items.append(items)
    return list_of_items

def get_iterable_converter(h5obj):
    converter = h5obj.attrs.get('iterable', '')
    return eval(converter) if converter else lambda obj: obj

def read_crs(group, name):
    subgroup = group[name]
    data = subgroup['data'].value
    index = subgroup['index'].value
    t = get_iterable_converter(subgroup)
    list_of_items = crs_to_list(data, index, items_container=t)
    return list_of_items

class Reader:

    def __init__(self, group, read_instance=None):
        self.group = group
        self.read_instance = read_instance

    def __call__(self, name, store_as='array'):
        if store_as == 'array':
            return self.array(name)
        elif store_as == 'scalar':
            return self.scalar(name)
        elif store_as == 'crs':
            return self.crs(name)
        elif store_as == 'dict':
            return self.dict(name)
        elif store_as == 'dict_crs':
            return self.dict_crs(name)
        elif store_as == 'yaml':
            return self.yaml(name)
        else:
            raise ValueError("No such type: %r" % (store_as,))

    def array(self, name):
        a = self.group[name].value
        if self.read_instance:
            setattr(self.read_instance, name,  a)
        else:
            return a

    def arrays(self, *names):
        for name in names:
            self.array(name)

    def scalar(self, name):
        s = self.group[name][()]
        if self.read_instance:
            setattr(self.read_instance, name,  s)
        else:
            return s

    def crs(self, name):
        list_of_items = read_crs(self.group, name)
        if self.read_instance:
            setattr(self.read_instance, name, list_of_items)
        else:
            return list_of_items

    def dict(self, name):
        subgroup = self.group[name]
        keys = self._read_obj_list(subgroup['keys'])
        values = self._read_obj_list(subgroup['values'])
        ordered = subgroup['ordered'][()]
        if ordered:
            d = dict(zip(keys,values))
        else:
            d = OrderedDict(zip(keys,values))
        if self.read_instance:
            setattr(self.read_instance, name, d)
        else:
            return d

    def dict_crs(self, name):
        subgroup = self.group[name]
        keys = self._read_obj_list(subgroup['keys'])
        values = read_crs(subgroup, 'values')
        ordered = subgroup['ordered'][()]
        if ordered:
            d = dict(zip(keys,values))
        else:
            d = OrderedDict(zip(keys,values))
        if self.read_instance:
            setattr(self.read_instance, name, d)
        else:
            return d

    def yaml(self, name):
        data = self.group[name].value
        obj = yaml.load(data)
        if self.read_instance:
            setattr(self.read_instance, name, obj)
        else:
            return obj
    
    def recurse(self, RecursivelyReadClass, name):
        inst = RecursivelyReadClass.read(self.group[name])
        if self.read_instance:
            setattr(self.read_instance, name, inst)
        else:
            return inst

    def _read_obj_list(self, dset):
        t = get_iterable_converter(dset)
        return [t(obj) for obj in dset.value]
