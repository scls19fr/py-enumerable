from ..visitors import IExpressionVisitor
from ..expressions import IExpression, ExpressionType


class SqliteExpressionVisitor(IExpressionVisitor):

    def __init__(self):
        self.__trees = {
            'select': None,
            'where': []
        }

    @property
    def sql(self):
        return self.__sql

    def visit(self, expression):
        if not isinstance(expression, IExpression):
            raise TypeError("expression arg needs to implement IExpression interface")
        node_type = expression.node_type
        if node_type == ExpressionType.SelectExpression:
            self._visit_select(expression)
        else:
            raise Exception(u"Cannot visit node: Unknown expression type {0}".format(node_type))

    def _visit_select(self, expression):
        self.__trees['select'] = expression.reduce()