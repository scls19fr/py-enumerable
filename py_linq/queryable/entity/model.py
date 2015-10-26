__author__ = 'Bruce.Fenske'

import inspect
from .column_types import Column
from .proxy import DynamicModelProxy

class Model(object):

    def __new__(cls, *args, **kwargs):
        return DynamicModelProxy(cls)

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
        columns = [
            (unicode(name), col) for name, col in inspect.getmembers(cls)
            if isinstance(col, Column)
        ]

        #Need to reorder the columns so that primary key is first for table creation. So just have this method
        #return the columns in the correct order everytime.
        pk_col = filter(lambda c: c[1].is_primary_key, columns)
        fk_col = filter(lambda c: c[1].foreign_key is not None, columns)
        rest = filter(lambda c: not c[1].is_primary_key and c[1].foreign_key is None, columns)
        columns = pk_col + fk_col + rest
        return [(name if col.column_name is None else col.column_name, col) for name, col in columns]

