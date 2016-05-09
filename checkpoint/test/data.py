from .. import Reader, Writer, create_reader

class FooArray:

    def __init__(self, data):
        self.data = data

    def write(self, group):
        writer = Writer(group, self)
        writer.array('data')

    @staticmethod
    def read(group):
        foo, reader = create_reader(FooArray, group)
        reader.array('data')
        return foo

class FooScalar:

    def __init__(self, data):
        self.data = data

    def write(self, group):
        writer = Writer(group, self)
        writer.scalar('data')

    @staticmethod
    def read(group):
        foo, reader = create_reader(FooScalar, group)
        reader.scalar('data')
        return foo

class FooCRS:

    def __init__(self, data):
        self.data = data

    def write(self, group):
        writer = Writer(group, self)
        writer.crs('data')

    @staticmethod
    def read(group):
        foo, reader = create_reader(FooCRS, group)
        reader.crs('data')
        return foo

class FooDict:

    def __init__(self, data):
        self.data = data

    def write(self, group):
        writer = Writer(group, self)
        writer.dict('data')

    @staticmethod
    def read(group):
        foo, reader = create_reader(FooDict, group)
        reader.dict('data')
        return foo

class FooDictCRS:

    def __init__(self, data):
        self.data = data

    def write(self, group):
        writer = Writer(group, self)
        writer.dict_crs('data')

    @staticmethod
    def read(group):
        foo, reader = create_reader(FooDict, group)
        reader.dict_crs('data')
        return foo

class FooYAML:

    def __init__(self, data):
        self.data = data

    def write(self, group):
        writer = Writer(group, self)
        writer.yaml('data')

    @staticmethod
    def read(group):
        foo, reader = create_reader(FooYAML, group)
        reader.yaml('data')
        return foo

class FooRecurse:

    def __init__(self, data):
        self.data = data

    def write(self, group):
        writer = Writer(group, self)
        writer.recurse('data')

    @staticmethod
    def read(group):
        foo, reader = create_reader(FooRecurse, group)
        reader.recurse(FooScalar, 'data')
        return foo
