from .. import Loader, Dumper, create_loader

class FooArray:

    def __init__(self, data):
        self.data = data

    def dump(self, group):
        dumper = Dumper(group, self)
        dumper.array('data')

    @staticmethod
    def load(group):
        foo, loader = create_loader(FooArray, group)
        loader.array('data')
        return foo

class FooScalar:

    def __init__(self, data):
        self.data = data

    def dump(self, group):
        dumper = Dumper(group, self)
        dumper.scalar('data')

    @staticmethod
    def load(group):
        foo, loader = create_loader(FooScalar, group)
        loader.scalar('data')
        return foo

class FooCRS:

    def __init__(self, data):
        self.data = data

    def dump(self, group):
        dumper = Dumper(group, self)
        dumper.crs('data')

    @staticmethod
    def load(group):
        foo, loader = create_loader(FooCRS, group)
        loader.crs('data')
        return foo

class FooDict:

    def __init__(self, data):
        self.data = data

    def dump(self, group):
        dumper = Dumper(group, self)
        dumper.dict('data')

    @staticmethod
    def load(group):
        foo, loader = create_loader(FooDict, group)
        loader.dict('data')
        return foo

class FooYAML:

    def __init__(self, data):
        self.data = data

    def dump(self, group):
        dumper = Dumper(group, self)
        dumper.yaml('data')

    @staticmethod
    def load(group):
        foo, loader = create_loader(FooYAML, group)
        loader.yaml('data')
        return foo

class FooRecurse:

    def __init__(self, data):
        self.data = data

    def dump(self, group):
        dumper = Dumper(group, self)
        dumper.recurse('data')

    @staticmethod
    def load(group):
        foo, loader = create_loader(FooRecurse, group)
        loader.recurse(FooScalar, 'data')
        return foo
