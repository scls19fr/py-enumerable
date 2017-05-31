from . import IExpressionVisitor
from ..expressions import SelectExpression
from ..expressions.unary import *
from ..expressions.binary import *


class SqlVisitor(IExpressionVisitor):
    def visit(self, expression):
        '''
        Visit method that parses the nodes in the AST
        :param expression: An AST object
        :return: a simpler expression. Goal is to eventually coalesce whole AST into StringExpression
        '''

        # Unary
        if isinstance(expression, StringExpression):
            return expression

        # Select
        elif isinstance(expression, SelectExpression):
            return self._visit_select(expression)

        # Binary
        elif isinstance(expression, TableExpression):
            return self.visit(StringExpression("{0} {1} {2}".format(self.visit(expression.left).value, self.visit(expression.operator).value, self.visit(expression.right).value)))
        else:
            raise NotImplementedError(
                u"expression {0} visitor method is not implemented".format(expression.__class__.__name__)
            )

    def _visit_select(self, expression):
        column_sql = []
        model_columns = expression.model.inspect_columns()
        if expression.func:
            model_columns = map(expression.func, model_columns)
        for name, column_instance in model_columns:
            column_sql.append("{0} AS {1}".format(
                name,
                column_instance.column_name if column_instance.column_name is not None else name
            ))
        return self.visit(StringExpression("SELECT {0}".format(", ".join(column_sql))))