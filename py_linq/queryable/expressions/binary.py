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

    @property
    def left(self):
        return self.children[0]

    @property
    def right(self):
        return self.children[1]
