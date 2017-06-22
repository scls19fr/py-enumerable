from . import BinaryExpression, SelectExpression, CountExpression
from .unary import *


class TableExpression(BinaryExpression):
    def __init__(self, model):
        left = SelectExpression(model)
        op = FromExpression(model)
        right = StringExpression(model, model.__table_name__)
        super(TableExpression, self).__init__(model, left, op, right)

    def can_reduce(self, node):
        if isinstance(node, SelectExpression) or isinstance(node, CountExpression):
            self.left = node
            return True
        return False


class ClauseExpression(BinaryExpression):
    def __init__(self, T, variable, logical_op, operand):
        super(ClauseExpression, self).__init__(T, variable, logical_op, operand)


class AndExpression(ClauseExpression):
    def __init__(self, T, variable, logical_op, operand):
        super(AndExpression, self).__init__(T, variable, logical_op, operand)


class OrExpression(ClauseExpression):
    def __init__(self, T, variable, logical_op, operand):
        super(AndExpression, self).__init__(T, variable, logical_op, operand)







