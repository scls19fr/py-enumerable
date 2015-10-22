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
    _column_proxies = {}

    def __init__(self, model):
        """
        Instantiates a proxy class of a given model. This proxy class auto-adds attributes from the model and
        instantiates a column proxy object for each attribute. The value for each attribute is set as well.
        :param model: A child class of a py_linq.queryable.entity.model.Model
        :return:
        """
        self._model = model
        self._add_model_columns()

    def __setattr__(self, key, value):
        super(DynamicModelProxy, self).__setattr__(key, value)
        try:
            proxy = self.columns[key]
        except KeyError:
            return
        proxy.value = value


    @property
    def model(self):
        return self._model

    @property
    def columns(self):
        return self._column_proxies

    def _add_model_columns(self):
        columns = [
            (unicode(name), col) for name, col in inspect.getmembers(self.model)
            if isinstance(col, Column)
        ]
        for name,col in columns:
            proxy = ColumnProxy(col, None)
            self.columns.setdefault(name, proxy)
            self.__dict__.setdefault(name, proxy.value)









