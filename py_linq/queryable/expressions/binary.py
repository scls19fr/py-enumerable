import abc
from ..expressions import *
from ..expressions.unary import ConstantExpression


class BinaryExpression(NaryExpression):
    __metaclass__ = abc.ABCMeta

    """
    Abstract implementation of Expression interface for BinaryExpression
    """
    def __init__(self, left, right):
        """

        :param unary1: UnaryExpression Instance
        :param unary2: UnaryExpression Instance
        """
        super(BinaryExpression, self).__init__(left, right)

    @abc.abstractproperty
    def node_type(self):
        raise NotImplementedError()

    @property
    def left(self):
        return self.children[0]

    @property
    def right(self):
        return self.children[1]


class AddExpression(BinaryExpression):
    """
    Implementation of add operation between expression
    """
    @property
    def node_type(self):
        return ExpressionType.Add

    def reduce(self):
        super(AddExpression, self).reduce()
        return self.left + self.right


class SubstractExpression(BinaryExpression):
    """
    Implementation of substract operation between expression
    """
    @property
    def node_type(self):
        return ExpressionType.Subtract

    def reduce(self):
        super(SubstractExpression, self).reduce()
        return self.left - self.right


class MultiplyExpression(BinaryExpression):
    """
    Implementation of multiply operation between expression
    """
    @property
    def node_type(self):
        return ExpressionType.Multiply

    def reduce(self):
        super(MultiplyExpression, self).reduce()
        return self.left * self.right


class DivideExpression(BinaryExpression):
    """
    Implementation of divide operation between expression
    """
    @property
    def node_type(self):
        return ExpressionType.Divide

    def reduce(self):
        super(DivideExpression, self).reduce()
        return self.left / self.right
