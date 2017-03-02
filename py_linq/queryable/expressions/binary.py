import abc
from ..expressions import Expression, ExpressionType
from ..expressions.unary import ConstantExpression


class BinaryExpression(Expression):
    __metaclass__ = abc.ABCMeta

    """
    Abstract implementation of Expression interface for BinaryExpression
    """
    def __init__(self, left, right):
        """

        :param unary1: UnaryExpression Instance
        :param unary2: UnaryExpression Instance
        """
        if not left.node_type == right.node_type:
            raise TypeError("type mismatch between unary expressions when instantiating binary expression")
        self._left = left
        self._right = right
        self._children = [self._left, self._right]

    @property
    def can_reduce(self):
        return True

    @abc.abstractproperty
    def node_type(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def reduce(self):
        raise NotImplementedError()

    def visit_children(self, expression_visitor):
        raise NotImplementedError()

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right


class AddExpression(BinaryExpression):
    """
    Implementation of add operation between expression
    """
    @property
    def node_type(self):
        return ExpressionType.Add

    def reduce(self):
        return self.left + self.right


class SubstractExpression(BinaryExpression):
    """
    Implementation of substract operation between expression
    """
    @property
    def node_type(self):
        return ExpressionType.Subtract

    def reduce(self):
        return self.left - self.right


class MultiplyExpression(BinaryExpression):
    """
    Implementation of multiply operation between expression
    """
    @property
    def node_type(self):
        return ExpressionType.Multiply

    def reduce(self):
        return self.left * self.right


class DivideExpression(BinaryExpression):
    """
    Implementation of divide operation between expression
    """
    @property
    def node_type(self):
        return ExpressionType.Divide

    def reduce(self):
        return self.left / self.right
