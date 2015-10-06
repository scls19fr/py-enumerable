__author__ = 'Bruce.Fenske'

import inspect
from .column_types import Column
from ...exceptions import InvalidArgumentError

class Model(object):

    @property
    def table_name(self):
        if not hasattr(self, '__table_name__'):
            raise AttributeError(unicode.format('No __table_name__ attribute set for {0}', self.__class__.__name__))
        return getattr(self, '__table_name__')

    @classmethod
    def inspect_columns(cls):
        """
        :return: list of (column_name, column instances) for the model
        """
        columns = [
            (unicode(name), col) for name, col in inspect.getmembers(cls)
            if isinstance(col, Column)
        ]
        return [(name if col.column_name is None else col.column_name, col) for name, col in columns]

