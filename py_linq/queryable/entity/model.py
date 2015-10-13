__author__ = 'Bruce.Fenske'

import inspect
from .column_types import Column
from ...py_linq import Enumerable

class Model(object):

    @classmethod
    def table_name(cls):
        if not hasattr(cls, '__table_name__'):
            raise AttributeError(unicode.format('No __table_name__ attribute set for {0}', cls.__name__))
        return getattr(cls, '__table_name__')

    @classmethod
    def inspect_columns(cls):
        """
        :return: list of (column_name, column instances) for the model
        """
        columns = Enumerable([
            (unicode(name), col) for name, col in inspect.getmembers(cls)
            if isinstance(col, Column)
        ]).order_by(lambda c: c[1].is_primary_key)
        return [(name if col.column_name is None else col.column_name, col) for name, col in columns]

