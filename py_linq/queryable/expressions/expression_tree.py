from ..expressions import *
from ..entity.model import Model


class ExpressionTree(NaryExpression):
    def __init__(self):
        super(ExpressionTree, self).__init__()

    def add_node(self, expression):
        if not isinstance(expression, IExpression):
            raise TypeError("Need to append IExpression instance as node in ExpressionTree")
        self.children.append(expression)


class ModelExpression(ExpressionTree):
    def __init__(self, klass):
        super(ModelExpression, self).__init__()
        if not issubclass(klass, Model):
            raise TypeError("klass arg must inherit from Model")
        self.__klass = klass

    @property
    def model(self):
        return self.__klass