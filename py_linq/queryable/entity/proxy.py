__author__ = 'Bruce.Fenske'

from .column_types import Column
from ...exceptions import InvalidArgumentError

class ColumnProxy(object):
    def __init__(self, column, value):
        if not isinstance(column, Column):
            raise InvalidArgumentError(u"column argument is not an instance of Column")
        self._column = column
        self._value = value

    @property
    def column(self):
        return self._column

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
