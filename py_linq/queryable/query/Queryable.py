from ..expressions.tree import ExpressionTree
from .QueryOptimizer import QueryOptimizer
from ..expressions import SelectExpression, CountExpression


class Queryable(object):
    __class_type__ = None
    def __init__(self, expression, query_provider):
        self.__expression_tree = ExpressionTree()
        self.__expression_tree.add_expression(expression)
        self.__provider = query_provider
        self.__class_type__ = expression.__class_type__

    @property
    def provider(self):
        return self.__provider

    @property
    def sql(self):
        optimzer = QueryOptimizer(self.__expression_tree)
        optimzer.optimize_tree()
        sql = []
        for ast in self.__expression_tree:
            sql.append(ast.visit(self.provider.provider_visitor).value)
        result = " ".join(sql)
        return result

    def select(self, func=None):
        self.__expression_tree.add_expression(SelectExpression(self.__class_type__, func))
        return self

    def count(self):
        self.__expression_tree.add_expression(CountExpression(self.__class_type__))
        return self.__provider.db_provider.execute_scalar(self.sql)






