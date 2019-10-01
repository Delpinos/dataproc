class Row(dict, object):
    def __setattr__(self, attr, value):
        self[attr] = value

    def __getattr__(self, attr):
        data = self.get(attr, None)
        if isinstance(data, dict):
            data = Row(data)
        return data

    def select(self, *args):
        item = {}
        for select in args:
            try:
                keys = str(select).split('.')
                key = keys.pop(0)
                v = self[key]
                alias = select.get_alias() if hasattr(select, 'get_alias') else None
                for key in keys:
                    v = v.get(key, None) if isinstance(v, dict) else None
                item[alias if alias is not None else key] = v
            except Exception:
                pass
        return Row(item)

    @classmethod
    def select_getter(self, *args):
        def getter(row):
            return Row(row).select(*args)

        return getter

    @classmethod
    def values_getter(self, *args):
        def getter(row):
            return list(Row(row).select(*args).values())

        return getter


class RowCreator(dict):
    __SELECT__ = []
    __ALIAS__ = None

    def __init__(self):
        self.__SELECT__ = []
        self.__ALIAS__ = None

    def alias(self, alias):
        self.__ALIAS__ = alias
        return self

    def get_alias(self):
        return self.__ALIAS__

    def __getattr__(self, attr):
        self.__SELECT__.append(attr)
        return self

    def __str__(self):
        return '.'.join(self.__SELECT__)
