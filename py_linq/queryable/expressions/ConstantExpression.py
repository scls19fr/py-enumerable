from ..expressions import *


class ConstantExpression(Expression):
    """
    Constant expression implementation
    """
    def __init__(self, value):
        self.__value = value

    @property
    def can_reduce(self):
        return False

    @property
    def node_type(self):
        return ExpressionType.Constant

    def reduce(self):
        return self

    def visit_children(self, expression_visitor):
        return self

    @property
    def value(self):
        return self.__value

    def __eq__(self, other):
        return self.value == other.value



