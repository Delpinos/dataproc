import copy
import hashlib
import pickle
import statistics

from bson.json_util import loads

from dataproc.model import Row, RowCreator


class Join(list):
    items = []

    def __init__(self, items=[]):
        self.items = items

    def appendjoin_inner_left_full(self, alias='join', data=[], where=lambda v1, v2: v1 == v2, row={}):
        app = False
        row[alias] = row.get(alias, [])
        for item in data:
            if where(row, item) is True:
                row[alias].append(item)
                self.items.append(Row(row))
            elif type in ['left', 'full']:
                self.items.append(Row(row))
        if app is False and type != 'inner':
            self.items.append(Row(row))

    def appendjoin_right_full(self, alias='join', data=[], where=lambda v1, v2: v1 == v2, item={}):
        app = False
        for row in data:
            row[alias] = row.get(alias, [])
            if where(row, item) is True:
                row[alias].append(item)
                self.items.append(Row(row))
            else:
                self.items.append(Row({alias: [item]}))
        if app is False:
            self.items.append(Row({alias: [item]}))

    def join_inner_left_full(self, alias='join', data=[], where=lambda v1, v2: v1 == v2, row={}):
        app = False
        row[alias] = row.get(alias, {})
        for item in data:
            if where(row, item) is True:
                row[alias] = item
                self.items.append(Row(row))
            elif type in ['left', 'full']:
                row[alias] = {}
                self.items.append(Row(row))
        if app is False and type != 'inner':
            self.items.append(Row(row))

    def join_right_full(self, alias='join', data=[], where=lambda v1, v2: v1 == v2, item={}):
        app = False
        for row in data:
            row[alias] = row.get(alias, {})
            if where(row, item) is True:
                tmp = copy.deepcopy(row)
                tmp[alias] = item
                self.items.append(Row(tmp))
            else:
                self.items.append(Row({alias: item}))
        if app is False:
            self.items.append(Row({alias: item}))

    def get_items(self):
        return self.items


class Executor(list):
    __SKIP_ = 0
    __PAGE__ = 1
    __DATA__ = []
    __SELECT__ = []
    __PIPELINE__ = []

    def __init__(self, pipeline=[]):
        if hasattr(pipeline, 'pipeline') and callable(getattr(pipeline, 'pipeline')):
            pipeline = pipeline.pipeline()
        self.__PIPELINE__ = list(pipeline)
        for row in self.__PIPELINE__:
            call = getattr(self, row[0], None)
            if callable(call):
                if len(row) == 1:
                    call()
                elif isinstance(row[1], dict):
                    call(**row[1])
                elif isinstance(row[1], (tuple, list)):
                    call(*tuple(row[1]))

    def from_list(self, data: list = []):
        try:
            self.__SELECT__ = []
            self.__DATA__ = list(map(Row, data))
        except Exception:
            pass
        finally:
            return self

    def from_bson(self, path):
        try:
            data = []
            with open(path, 'r') as file:
                for line in file:
                    try:
                        tmp = loads(line)
                    except Exception as e:
                        print(e)
                        tmp = None
                    if tmp is not None:
                        if isinstance(tmp, list):
                            for row in tmp:
                                data.append(row)
                        else:
                            data.append(tmp)
            self.from_list(data)
        except Exception:
            pass
        finally:
            return self

    def __getattr__(self, attr):
        row = RowCreator()
        getattr(row, attr)
        return row

    def select(self, *args):
        self.__DATA__ = list(map(lambda row: Row(row).select(*args), self.__DATA__))
        self.__SELECT__ = []
        return self

    def reduce(self, *args):
        data = {}
        args = list(map(str, args))
        for item in self.__DATA__:
            row = {"__COUNT__": 0}
            for key in item.keys():
                if key in args:
                    continue
                row[key] = item.get(key, None)
            hash = self.hash(row)
            data[hash] = data.get(hash, row)
            data[hash]['__COUNT__'] = data[hash].get('__COUNT__', 0)
            data[hash]['__COUNT__'] += 1
            for key in args:
                data[hash]['__VALUES__'] = data[hash].get('__VALUES__', {})
                data[hash]['__VALUES__'][key] = data[hash]['__VALUES__'].get(key, [])
                data[hash]['__VALUES__'][key].append(item.get(key, None))
        self.__DATA__ = list(map(Row, data.values()))
        self.__SELECT__ = []
        return self

    def function(self, *args):
        def _map(fields: list, fnc: lambda v: v, data: list = []):
            if callable(fnc):
                for row in data:
                    for field in fields:
                        field = str(field)
                        row['__VALUES__'] = row.get('__VALUES__', {})
                        row[field] = fnc(row['__VALUES__'].get(field, None))
            return data

        pipe = list(args)
        fnc = pipe.pop(-1)
        self.__DATA__ = _map(pipe, fnc, self.__DATA__)
        return self

    def custom(self, alias='custom', fnc=lambda v: v):
        alias = str(alias)

        def _map(row):
            if callable(fnc):
                try:
                    row[alias] = fnc(row)
                except Exception:
                    row[alias] = row.get(alias, None)
            return row

        self.__DATA__ = list(map(_map, self.__DATA__))
        self.__SELECT__ = []
        return self

    def map(self, *args):
        def _map(row):
            for fnc in args:
                if callable(fnc):
                    try:
                        fnc(row)
                    except Exception:
                        continue
            return row

        self.__DATA__ = list(map(_map, self.__DATA__))
        self.__SELECT__ = []
        return self

    def count(self, name):
        name = str(name)
        for row in self.__DATA__:
            row[name] = row.get('__COUNT__', 0)
        return self

    def list(self, *args):
        for row in self.__DATA__:
            for field in args:
                alias = field.get_alias() if isinstance(field, RowCreator) else str(field)
                field = str(field)
                alias = field if alias is None else alias
                row['__VALUES__'] = row.get('__VALUES__', {})
                items = [i for i in row['__VALUES__'].get(field, []) if i is not None]
                row[alias] = list(items) if len(items) > 0 else None
        return self

    def distinct(self, *args):
        for row in self.__DATA__:
            for field in args:
                alias = field.get_alias() if isinstance(field, RowCreator) else str(field)
                field = str(field)
                alias = field if alias is None else alias
                row['__VALUES__'] = row.get('__VALUES__', {})
                items = [i for i in row['__VALUES__'].get(field, []) if i is not None]
                row[alias] = list(set(list(items))) if len(items) > 0 else None
        return self

    def min(self, *args):
        for row in self.__DATA__:
            for field in args:
                alias = field.get_alias() if isinstance(field, RowCreator) else str(field)
                field = str(field)
                alias = field if alias is None else alias
                row['__VALUES__'] = row.get('__VALUES__', {})
                items = [i for i in row['__VALUES__'].get(field, []) if i is not None]
                row[alias] = min(items) if len(items) > 0 else None
        return self

    def max(self, *args):
        for row in self.__DATA__:
            for field in args:
                alias = field.get_alias() if isinstance(field, RowCreator) else str(field)
                field = str(field)
                alias = field if alias is None else alias
                row['__VALUES__'] = row.get('__VALUES__', {})
                items = [i for i in row['__VALUES__'].get(field, []) if i is not None]
                row[alias] = max(items) if len(items) > 0 else None
        return self

    def sum(self, *args):
        for row in self.__DATA__:
            for field in args:
                alias = field.get_alias() if isinstance(field, RowCreator) else str(field)
                field = str(field)
                alias = field if alias is None else alias
                row['__VALUES__'] = row.get('__VALUES__', {})
                items = [i for i in row['__VALUES__'].get(field, []) if i is not None]
                row[alias] = sum(items) if len(items) > 0 else None
        return self

    def mean(self, *args):
        for row in self.__DATA__:
            for field in args:
                alias = field.get_alias() if isinstance(field, RowCreator) else str(field)
                field = str(field)
                alias = field if alias is None else alias
                row['__VALUES__'] = row.get('__VALUES__', {})
                items = [i for i in row['__VALUES__'].get(field, []) if i is not None]
                row[alias] = statistics.mean(items) if len(items) > 0 else None
        return self

    def median(self, *args):
        for row in self.__DATA__:
            for field in args:
                alias = field.get_alias() if isinstance(field, RowCreator) else str(field)
                field = str(field)
                alias = field if alias is None else alias
                row['__VALUES__'] = row.get('__VALUES__', {})
                items = [i for i in row['__VALUES__'].get(field, []) if i is not None]
                row[alias] = statistics.median(items) if len(items) > 0 else None
        return self

    def data(self):
        for row in self.__DATA__:
            for index in ['__COUNT__', '__VALUES__']:
                try:
                    del row[index]
                except Exception:
                    continue
        return self.__DATA__

    def page(self, page: int = 1):
        self.__PAGE__ = page
        return self

    def skip(self, skip: int = 0):
        self.__SKIP__ = skip
        return self

    def filter(self, *args):
        cls = []
        for fnc in args:
            if callable(fnc):
                cls.append(fnc)

        def _filter(row):
            for fnc in cls:
                if fnc(row):
                    return True
            return False

        if len(args) > 0:
            self.__DATA__ = list(filter(_filter, self.__DATA__))
        return self

    def limit(self, limit: int = 1000):
        self.__LIMIT__ = limit
        _len = len(self.__DATA__)
        if isinstance(self.__SKIP__, int) and self.__SKIP__ > 0:
            if _len > self.__SKIP__:
                _start = (self.__SKIP__ - 1)
                self.__DATA__ = self.__DATA__[_start:(_start + limit)]
            else:
                self.__DATA__ = []
            self.__SKIP__ = 0
        elif isinstance(self.__PAGE__, int) and self.__PAGE__ > 1:
            self.__SKIP__ = ((self.__PAGE__ - 1) * limit) + 1
            self.__PAGE__ = 1
            return self.limit(limit)
        else:
            self.__DATA__ = self.__DATA__[0:limit]
        self.__SELECT__ = []
        return self

    def inner_appendjoin(self, alias='inner_appendjoin', data=[], where=lambda v1, v2: v1 == v2):
        return self.appendjoin(alias, data, where, 'inner')

    def left_appendjoin(self, alias='left_appendjoin', data=[], where=lambda v1, v2: v1 == v2):
        return self.appendjoin(alias, data, where, 'left')

    def right_appendjoin(self, alias='right_appendjoin', data=[], where=lambda v1, v2: v1 == v2):
        return self.appendjoin(alias, data, where, 'right')

    def full_appendjoin(self, alias='full_appendjoin', data=[], where=lambda v1, v2: v1 == v2):
        return self.appendjoin(alias, data, where, 'full')

    def inner_join(self, alias='inner_join', data=[], where=lambda v1, v2: v1 == v2):
        return self.join(alias, data, where, 'inner')

    def left_join(self, alias='left_join', data=[], where=lambda v1, v2: v1 == v2):
        return self.join(alias, data, where, 'left')

    def right_join(self, alias='right_join', data=[], where=lambda v1, v2: v1 == v2):
        return self.join(alias, data, where, 'right')

    def full_join(self, alias='full_join', data=[], where=lambda v1, v2: v1 == v2):
        return self.join(alias, data, where, 'full')

    def appendjoin(self, alias='join', data=[], where=lambda v1, v2: v1 == v2, type='inner'):
        alias = str(alias)
        items = []
        if hasattr(data, 'data') and callable(getattr(data, 'data')):
            data = data.data()

        if not callable(where):
            return self

        join = Join(items)

        if type in ['inner', 'left', 'full']:
            list(map(lambda row: join.appendjoin_inner_left_full(alias, data, where, row), self.__DATA__))

        if type in ['right', 'full']:
            list(map(lambda row: join.appendjoin_right_full(alias, self.__DATA__, where, row), data))

        self.__DATA__ = join.get_items()
        self.__SELECT__ = []
        return self

    def join(self, alias='join', data=[], where=lambda v1, v2: v1 == v2, type='inner'):
        alias = str(alias)
        items = []
        if hasattr(data, 'data') and callable(getattr(data, 'data')):
            data = data.data()

        if not callable(where):
            return self

        join = Join(items)

        if type in ['inner', 'left', 'full']:
            list(map(lambda row: join.join_inner_left_full(alias, data, where, row), self.__DATA__))

        if type in ['right', 'full']:
            list(map(lambda row: join.join_right_full(alias, self.__DATA__, where, row), data))

        self.__DATA__ = join.get_items()
        self.__SELECT__ = []
        return self

    def sort(self, **sort):
        order = []
        asc = set()
        desc = set()

        for k in sort.keys():
            if sort[k] in ['0', '-1', 'desc', 'DESC']:
                if len(asc) > 0:
                    order.append([tuple(asc), False])
                    asc = set()
                desc.add(k)
            else:
                if len(desc) > 0:
                    order.append([tuple(desc), True])
                    desc = set()
                asc.add(k)

        if len(asc) > 0:
            order.append([tuple(asc), False])
        if len(desc) > 0:
            order.append([tuple(desc), True])

        for sort in order:
            self.__DATA__ = sorted(self.__DATA__, key=Row.values_getter(*sort[0]), reverse=sort[1])

        return self

    def hash(self, data):
        return hashlib.sha1(str(pickle.dumps(data)).encode()).hexdigest()
