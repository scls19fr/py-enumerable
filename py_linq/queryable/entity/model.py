__author__ = 'Bruce.Fenske'

import inspect

class Model(object):

    @property
    def table_name(self):
        if not hasattr(self, '__table_name__'):
            raise AttributeError(unicode.format('No __table_name__ attribute set for {0}', self.__class__.__name__))
        return getattr(self, '__table_name__')

    def inspect_columns(self):
        """
        :return: list of (column_name, column instances) for the model
        """
        columns = [
            (name, col) for name, col in inspect.getmembers(self)
            if isinstance(col, Column)
        ]
        return [(name if col.column_name is None else col.column_name, col) for name, col in columns]


class Column(object):

    def __init__(self, column_type, column_name=None):
        self._column_name = column_name
        self._column_type = column_type

    @property
    def column_type(self):
        return type(self._column_type)

    @property
    def column_name(self):
        if self._column_name is None or self._column_name == '' or len(self._column_name) == 0:
            return None
        return self._column_name
