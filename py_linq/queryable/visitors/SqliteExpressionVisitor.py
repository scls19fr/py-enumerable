from ..visitors import IExpressionVisitor, SqlVisitorResultModel
from ..expressions import IExpression, ExpressionType


class SqliteExpressionVisitor(IExpressionVisitor):

    def __init__(self):
        self.__result = SqlVisitorResultModel()

    def visit(self, expression):
        if not isinstance(expression, IExpression):
            raise TypeError("expression arg needs to implement IExpression interface")
        node_type = expression.node_type
        if node_type == ExpressionType.SelectExpression:
            self._visit_select(expression)
        if node_type == ExpressionType.ModelExpression:
            self._visit_model(expression)
        else:
            raise Exception(u"Cannot visit node: Unknown expression type {0}".format(node_type))

    def _visit_select(self, expression):
        self.sql_expression_result.projection = expression.reduce()

    def _visit_model(self, expression):
        self.sql_expression_result.source = expression.model.table_name()

    @property
    def sql_expression_result(self):
        return self.__result

