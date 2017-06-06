from ..expressions.tree import ExpressionTree
from .QueryOptimizer import QueryOptimizer
from ..expressions import SelectExpression, CountExpression
from ..expressions.unary import TakeExpression


class Queryable(object):
    __class_type__ = None

    def __init__(self, expression, query_provider):
        self.__expression_tree = ExpressionTree()
        self.__expression_tree.add_expression(expression)
        self.__provider = query_provider
        self.__class_type__ = expression.__class_type__

    def __iter__(self):
        cursor = self.__provider.db_provider.connection.cursor()
        print self.sql
        cursor.execute(self.sql)
        for r in cursor:
            if len(r) == 1:
                yield r[0]
            yield r


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
        self.__expression_tree.add_expression(TakeExpression(self.__class_type__, limit))
        return self

    def as_enumerable(self):
        raise NotImplementedError()








