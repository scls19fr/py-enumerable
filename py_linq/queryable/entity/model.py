__author__ = 'Bruce.Fenske'

import inspect
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
            (name, col) for name, col in inspect.getmembers(cls)
            if isinstance(col, Column)
        ]
        return [(name if col.column_name is None else col.column_name, col) for name, col in columns]


class Column(object):

    def __init__(self, column_type, column_name=None, foreign_key=None, is_primary_key=False, is_nullable=False, is_unique=False):
        self._column_name = column_name
        self._column_type = column_type
        self._foreign_key = foreign_key
        self._is_primary_key = is_primary_key
        self._is_nullable = is_nullable
        self._is_unique = is_unique

    @property
    def column_type(self):
        return type(self._column_type)

    @property
    def column_name(self):
        if self._column_name is None or self._column_name == u'' or len(self._column_name) == 0:
            return None
        return self._column_name

    @property
    def has_foreign_key(self):
        return self._foreign_key != None

    @property
    def is_primary_key(self):
        return self._is_primary_key

    @property
    def is_nullable(self):
        return self._is_nullable

    @property
    def is_unique(self):
        return self.is_unique

    def generate_col_sql(self, provider, column_name):
        """
        :param provider: A DbConnectionBase type
        :return: SQL statement for column as text
        """
        try:
            column_type = provider.provider_data_types[self.column_type]
        except KeyError:
            raise KeyError(u"{0} is not a valid column data type".format(self.column_type))
        sql = unicode.format("{0} {1}", column_name, column_type)
        sql = unicode.format(" {0} NULL", sql) if self.is_nullable else unicode.format(" {0} NOT NULL", sql)
        if self.is_primary_key:
            sql = unicode.format(" {0} PRIMARY KEY", sql)
        if self.is_unique and not self.is_primary_key:
            sql = unicode.format(" {0} UNIQUE", sql)
        #TODO: Add foreign key syntax here
        return sql

