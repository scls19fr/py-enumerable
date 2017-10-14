from ..expressions import *
from ..entity.proxy import DynamicModelProxy
from py_linq import Enumerable
from py_linq.exceptions import NoElementsError


class Queryable(object):
    __class_type__ = None

    def __init__(self, expression, query_provider):
        self.__exp = expression
        self.__provider = query_provider

    def __iter__(self):
        raise NotImplementedError()

    @property
    def provider(self):
        return self.__provider

    @property
    def type(self):
        return self.expression.type

    @property
    def expression(self):
        return self.__exp

    @property
    def sql(self):
        raise NotImplementedError()

    def select(self, func):
        self.__exp = UnaryExpression(SelectExpression(self.type, func), self.expression)
        return self

    def count(self):
        raise NotImplementedError()

    def take(self, limit):
        raise NotImplementedError()

    def skip(self, offset):
        raise NotImplementedError()

    def first(self):
        raise NotImplementedError()

    def first_or_default(self):
        try:
            return self.first()
        except NoElementsError:
            return None

    def to_list(self):
        raise NotImplementedError()









