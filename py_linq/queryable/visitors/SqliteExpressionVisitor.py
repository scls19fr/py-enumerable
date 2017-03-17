from ..visitors import IExpressionVisitor, SqlVisitorResultModel
from ..expressions import IExpression
from ..expressions.sql import *
from ..expressions.expression_tree import ModelExpression


class SqliteExpressionVisitor(IExpressionVisitor):

    def __init__(self):
        self.__result = SqlVisitorResultModel()

    def visit(self, expression):
        if not isinstance(expression, IExpression):
            raise TypeError("expression arg needs to implement IExpression interface")

        if isinstance(expression, SelectExpression):
            self._visit_select(expression)
        elif isinstance(expression, ModelExpression):
            self._visit_model(expression)
        else:
            raise Exception(u"Cannot visit node: Unknown expression type {0}".format(expression.__class__.__name__))

    def _visit_select(self, expression):
        self.sql_expression_result.projection = expression.reduce()

    def _visit_model(self, expression):
        self.sql_expression_result.source = expression.model.table_name()
        if len(filter(lambda e: isinstance(e, SelectExpression), expression.children)) == 0:
            expression.add_node(SelectExpression(expression))

    @property
    def sql_expression_result(self):
        return self.__result

