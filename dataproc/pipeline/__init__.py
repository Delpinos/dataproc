from dataproc.executor import Executor
from dataproc.model import RowCreator


class Pipeline(list):
    __PIPELINE__ = []
    __REDUCE__ = []

    def __init__(self, pipeline=[]):
        if hasattr(pipeline, 'pipeline') and callable(getattr(pipeline, 'pipeline')):
            pipeline = pipeline.pipeline()
        self.__PIPELINE__ = list(pipeline)

    def __getattr__(self, attr):
        row = RowCreator()
        getattr(row, attr)
        return row

    def __groupfunction__(self):
        return ['sum', 'mean', 'median', 'list', 'distinct', 'min', 'max']

    def from_list(self, *args, **kargs):
        kargs['data'] = list(kargs.get('data', args[0] if len(args) >= 1 else []))
        self.__PIPELINE__.append(['from_list', kargs])
        return self

    def from_bson(self, *args, **kargs):
        kargs['path'] = str(kargs.get('path', args[0] if len(args) >= 1 else ''))
        self.__PIPELINE__.append(['from_bson', kargs])
        return self

    def select(self, *args, **kargs):
        self.__PIPELINE__.append(['select', args])
        return self

    def reduce(self, *args):
        self.__REDUCE__ = []
        self.__PIPELINE__.append(['reduce', args])
        return self

    def function(self, *args):
        self.__PIPELINE__.append(['function', args])
        return self

    def custom(self, *args, **kargs):
        kargs['alias'] = kargs.get('alias', args[0] if len(args) >= 1 else 'custom')
        kargs['fnc'] = kargs.get('fnc', args[1] if len(args) >= 1 else lambda v: v)
        self.__PIPELINE__.append(['custom', kargs])
        return self

    def map(self, *args):
        self.__PIPELINE__.append(['map', args])
        return self

    def count(self, name, *args):
        self.__PIPELINE__.append(['count', args])
        return self

    def list(self, *args):
        self.__PIPELINE__.append(['list', args])
        return self

    def distinct(self, *args):
        self.__PIPELINE__.append(['distinct', args])
        return self

    def min(self, *args):
        self.__PIPELINE__.append(['min', args])
        return self

    def max(self, *args):
        self.__PIPELINE__.append(['max', args])
        return self

    def sum(self, *args):
        self.__PIPELINE__.append(['sum', args])
        return self

    def mean(self, *args):
        self.__PIPELINE__.append(['mean', args])
        return self

    def median(self, *args):
        self.__PIPELINE__.append(['median', args])
        return self

    def page(self, *args, **kargs):
        kargs['page'] = int(kargs.get('page', args[0] if len(args) >= 1 else 1))
        self.__PIPELINE__.append(['page', kargs])
        return self

    def skip(self, *args, **kargs):
        kargs['skip'] = int(kargs.get('skip', args[0] if len(args) >= 1 else 0))
        self.__PIPELINE__.append(['skip', kargs])
        return self

    def filter(self, *args):
        self.__PIPELINE__.append(['filter', args])
        return self

    def limit(self, *args, **kargs):
        kargs['limit'] = int(kargs.get('limit', args[0] if len(args) >= 1 else 1000))
        self.__PIPELINE__.append(['limit', kargs])
        return self

    def inner_appendjoin(self, *args, **kargs):
        kargs['alias'] = str(kargs.get('alias', args[0] if len(args) >= 1 else 'inner_appendjoin'))
        kargs['data'] = kargs.get('data', args[1] if len(args) >= 2 else [])
        kargs['where'] = kargs.get('where', args[2] if len(args) >= 3 else lambda v1, v2: v1 == v2)
        self.__PIPELINE__.append(['inner_appendjoin', kargs])
        return self

    def left_appendjoin(self, *args, **kargs):
        kargs['alias'] = str(kargs.get('alias', args[0] if len(args) >= 1 else 'left_appendjoin'))
        kargs['data'] = kargs.get('data', args[1] if len(args) >= 2 else [])
        kargs['where'] = kargs.get('where', args[2] if len(args) >= 3 else lambda v1, v2: v1 == v2)
        self.__PIPELINE__.append(['left_appendjoin', kargs])
        return self

    def right_appendjoin(self, *args, **kargs):
        kargs['alias'] = str(kargs.get('alias', args[0] if len(args) >= 1 else 'right_appendjoin'))
        kargs['data'] = kargs.get('data', args[1] if len(args) >= 2 else [])
        kargs['where'] = kargs.get('where', args[2] if len(args) >= 3 else lambda v1, v2: v1 == v2)
        self.__PIPELINE__.append(['right_appendjoin', kargs])
        return self

    def full_appendjoin(self, *args, **kargs):
        kargs['alias'] = str(kargs.get('alias', args[0] if len(args) >= 1 else 'full_appendjoin'))
        kargs['data'] = kargs.get('data', args[1] if len(args) >= 2 else [])
        kargs['where'] = kargs.get('where', args[2] if len(args) >= 3 else lambda v1, v2: v1 == v2)
        self.__PIPELINE__.append(['full_appendjoin', kargs])
        return self

    def inner_join(self, *args, **kargs):
        kargs['alias'] = str(kargs.get('alias', args[0] if len(args) >= 1 else 'inner_join'))
        kargs['data'] = kargs.get('data', args[1] if len(args) >= 2 else [])
        kargs['where'] = kargs.get('where', args[2] if len(args) >= 3 else lambda v1, v2: v1 == v2)
        self.__PIPELINE__.append(['inner_join', kargs])
        return self

    def left_join(self, *args, **kargs):
        kargs['alias'] = str(kargs.get('alias', args[0] if len(args) >= 1 else 'left_join'))
        kargs['data'] = kargs.get('data', args[1] if len(args) >= 2 else [])
        kargs['where'] = kargs.get('where', args[2] if len(args) >= 3 else lambda v1, v2: v1 == v2)
        self.__PIPELINE__.append(['left_join', kargs])
        return self

    def right_join(self, *args, **kargs):
        kargs['alias'] = str(kargs.get('alias', args[0] if len(args) >= 1 else 'right_join'))
        kargs['data'] = kargs.get('data', args[1] if len(args) >= 2 else [])
        kargs['where'] = kargs.get('where', args[2] if len(args) >= 3 else lambda v1, v2: v1 == v2)
        self.__PIPELINE__.append(['right_join', kargs])
        return self

    def full_join(self, *args, **kargs):
        kargs['alias'] = str(kargs.get('alias', args[0] if len(args) >= 1 else 'full_join'))
        kargs['data'] = kargs.get('data', args[1] if len(args) >= 2 else [])
        kargs['where'] = kargs.get('where', args[2] if len(args) >= 3 else lambda v1, v2: v1 == v2)
        self.__PIPELINE__.append(['full_join', kargs])
        return self

    def appendjoin(self, *args, **kargs):
        kargs['alias'] = str(kargs.get('alias', args[0] if len(args) >= 1 else 'appendjoin'))
        kargs['data'] = kargs.get('data', args[1] if len(args) >= 2 else [])
        kargs['where'] = kargs.get('where', args[2] if len(args) >= 3 else lambda v1, v2: v1 == v2)
        kargs['type'] = str(kargs.get('type', args[3] if len(args) >= 4 else 'inner'))
        self.__PIPELINE__.append(['appendjoin', kargs])
        return self

    def join(self, *args, **kargs):
        kargs['alias'] = str(kargs.get('alias', args[0] if len(args) >= 1 else 'join'))
        kargs['data'] = kargs.get('data', args[1] if len(args) >= 2 else [])
        kargs['where'] = kargs.get('where', args[2] if len(args) >= 3 else lambda v1, v2: v1 == v2)
        kargs['type'] = str(kargs.get('type', args[3] if len(args) >= 4 else 'inner'))
        self.__PIPELINE__.append(['join', kargs])
        return self

    def sort(self, *args, **kargs):
        kargs = kargs if kargs is not None else args[0]
        self.__PIPELINE__.append(['sort', kargs])
        return self

    def pipeline(self):
        pipeline = []
        reduce = 0
        reduce_list = []
        olds = []
        for pipe in self.__PIPELINE__:
            if pipe[0] == 'select':
                if len(olds) > 0:
                    pipeline.append(['reduce', list(set(list(map(str, reduce_list))))])
                    [pipeline.append(old) for old in olds]
                    olds = []
                reduce = 0
                pipeline.append(pipe)
            elif pipe[0] == 'reduce':
                reduce = 1
                pipeline.append(pipe)
            elif pipe[0] in self.__groupfunction__() and reduce in [0, 2]:
                [reduce_list.append(str(arg)) for arg in pipe[1]]
                reduce = 2
                olds.append(pipe)
            elif reduce == 2:
                pipeline.append(['reduce', list(set(list(map(str, reduce_list))))])
                [pipeline.append(old) for old in olds]
                pipeline.append(pipe)
                reduce = 0
                olds = []
            else:
                pipeline.append(pipe)

        if len(olds) > 0:
            pipeline.append(['reduce', list(set(list(map(str, reduce_list))))])
            [pipeline.append(old) for old in olds]

        return pipeline

    def data(self):
        return Executor(self).data()
