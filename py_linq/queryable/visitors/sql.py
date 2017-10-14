from . import IExpressionVisitor
from ..expressions import LambdaExpression


class SqlVisitor(IExpressionVisitor):

    def visit_UnaryExpression(self, expression):
        return u"{0} {1}".format(expression.op.visit(self), expression.exp.visit(self))

    def visit_SelectExpression(self, expression):
        t = LambdaExpression.parse(expression.type, expression.func)
        return u"SELECT {0}".format(t.body.sql)

    def visit_TableExpression(self, expression):
        return u"FROM {0}".format(expression.type.table_name)

