from ..expressions.tree import ExpressionTree
from .QueryOptimizer import QueryOptimizer
from ..expressions import *
from ..expressions.unary import *
from ..entity.proxy import DynamicModelProxy
from py_linq import Enumerable
from py_linq.exceptions import NoElementsError


class Queryable(object):
    __class_type__ = None

    def __init__(self, expression, query_provider):
        self.__expression_tree = ExpressionTree()
        self.__expression_tree.add_expression(expression)
        self.__provider = query_provider
        self.__class_type__ = expression.__class_type__

    def __iter__(self):
        cursor = self.__provider.db_provider.connection.cursor()
        num_cols = self.__class_type__.inspect_columns()
        cursor.execute(self.sql)
        for r in cursor:
            # if returning just one column
            if len(r) == 1:
                yield r[0]
            # if returning all the columns
            elif len(r) == len(num_cols):
                proxy = DynamicModelProxy(self.__class_type__)
                for i in range(0, len(r), 1):
                    result_value = r[i]
                    k = cursor.description[i][0]
                    proxy.__setattr__(k, result_value)
                yield proxy
            # TODO: if returning a subset of columns
            else:
                raise NotImplementedError()

    @property
    def provider(self):
        return self.__provider

    @property
    def sql(self):
        optimizer = QueryOptimizer(self.__expression_tree)
        optimizer.optimize_tree()
        sql = []
        for ast in self.__expression_tree:
            sql.append(ast.visit(self.provider.provider_visitor).value)
        result = u" ".join(sql)
        return result

    def select(self, func=None):
        self.__expression_tree.add_expression(SelectExpression(self.__class_type__, func))
        return self

    def count(self):
        self.__expression_tree.add_expression(CountExpression(self.__class_type__))
        return self.__provider.db_provider.execute_scalar(self.sql)

    def take(self, limit):
        self.__expression_tree.add_expression(SkipTakeExpression(self.__class_type__, limit=limit))
        return self

    def skip(self, offset):
        self.__expression_tree.add_expression(SkipTakeExpression(self.__class_type__, offset=offset))
        return self

    def first(self):
        self.__expression_tree.add_expression(SkipTakeExpression(self.__class_type__, limit=1))
        return Enumerable(self).first()

    def first_or_default(self):
        try:
            return self.first()
        except NoElementsError:
            return None

    def to_list(self):
        return Enumerable(self).to_list()









