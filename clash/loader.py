import yaml

import numpy as np

def create_loader(LoadedClass, group):
    loaded_instance = LoadedClass.__new__(LoadedClass)
    loader = Loader(group, loaded_instance)
    return loaded_instance, loader
    
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

class Loader:

    def __init__(self, group, loaded_instance, load_method='load'):
        self.group = group
        self.loaded_instance = loaded_instance
        self.load_method = load_method

    def array(self, name):
        a = self.group[name].value
        setattr(self.loaded_instance, name,  a)

    def arrays(self, *names):
        for name in names:
            self.array(name)

    def scalar(self, name):
        s = self.group[name][()]
        setattr(self.loaded_instance, name,  s)

    def crs(self, name):
        subgroup = self.group[name]
        data = subgroup['data'].value
        index = subgroup['index'].value
        t = self._get_iterable_converter(subgroup)
        list_of_items = crs_to_list(data, index, items_container=t)
        setattr(self.loaded_instance, name, list_of_items)

    def dict(self, name, dict_type=dict):
        subgroup = self.group[name]
        keys = self._load_obj_list(subgroup['keys'])
        values = self._load_obj_list(subgroup['values'])
        d = dict_type(zip(keys,values))
        setattr(self.loaded_instance, name, d)

    def yaml(self, name):
        data = self.group[name].value
        obj = yaml.load(data)
        setattr(self.loaded_instance, name, obj)
    
    def recurse(self, RecursivelyLoadedClass, name):
        inst = RecursivelyLoadedClass.load(self.group[name])
        setattr(self.loaded_instance, name, inst)

    def _load_obj_list(self, dset):
        t = self._get_iterable_converter(dset)
        return [t(obj) for obj in dset.value]

    def _get_iterable_converter(self, h5obj):
        type_name = h5obj.attrs.get('iterable', '')
        return eval(type_name) if type_name else lambda obj: obj
