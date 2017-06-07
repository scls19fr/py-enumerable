from . import IExpressionVisitor
from ..expressions import *
from ..expressions.unary import *
from ..expressions.binary import *
from py_linq import Enumerable


class SqlVisitor(IExpressionVisitor):
    def visit(self, expression):
        """
        Visit method that parses the nodes in the AST
        :param expression: An AST object
        :return: a simpler expression. Goal is to eventually coalesce whole AST into StringExpression
        """
        # Unary
        if isinstance(expression, StringExpression):
            return expression
        elif isinstance(expression, CountExpression):
            return self.visit(StringExpression(expression.__class_type__, u"SELECT COUNT(*)"))
        elif isinstance(expression, SkipTakeExpression):
            return self.visit(StringExpression(expression.__class_type__, u"LIMIT {0} OFFSET {1}".format(expression.limit, expression.offset)))
        # Select
        elif isinstance(expression, SelectExpression):
            return self._visit_select(expression)

        # Binary
        elif isinstance(expression, BinaryExpression):
            return self.visit(
                StringExpression(
                    expression.__class_type__,
                    u"{0} {1} {2}".format(
                        self.visit(expression.left).value,
                        self.visit(expression.operator).value,
                        self.visit(expression.right).value
                    )
                )
            )
        else:
            raise NotImplementedError(
                u"expression {0} visitor method is not implemented".format(expression.__class__.__name__)
            )

    def _visit_select(self, expression):
        column_sql = []
        model_columns = expression.__class_type__.inspect_columns()
        if expression.func is not None:
            model_columns = map(expression.func, model_columns)
        for col in model_columns:
            column_sql.append(u"{0} AS {1}".format(
                col[0],
                col[1].column_name if col[1].column_name is not None else col[0]
            ))
        return self.visit(StringExpression(expression.__class_type__, u"SELECT {0}".format(u", ".join(column_sql))))
