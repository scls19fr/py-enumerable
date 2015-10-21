__author__ = 'Bruce.Fenske'

import inspect
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
        if type(value) != self.column.column_type:
            raise InvalidArgumentError(u"{0} does not equal {1}".format(value, self.column.column_type))
        self._value = value


class DynamicModelProxy(object):
    def __init__(self, model):
        """
        Instantiates a proxy class of a given model. This proxy class auto-adds attributes from the model and
        instantiates a column proxy object for each attribute. The value for each attribute is set as well.
        :param model: A child class of a py_linq.queryable.entity.model.Model
        :return:
        """
        self._model = model
        self.__add_attributes()

    @property
    def model(self):
        return self._model

    def __add_attributes(self):
        attrs = {}
        columns = [
            (unicode(name), col) for name, col in inspect.getmembers(self.model)
            if isinstance(col, Column)
        ]
        for name, col in columns:
            attrs.setdefault(name, ColumnProxy(col, None))
        self.__dict__.update(attrs)
        self.__make_properties(attrs)

    def __make_properties(self, attrs):
        for k,v in attrs:
            raise NotImplementedError()

