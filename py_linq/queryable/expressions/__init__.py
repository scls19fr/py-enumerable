import abc


class AST(object):
    @abc.abstractproperty
    def can_reduce(self):
        return NotImplementedError()

    def reduce(self):
        return self._reduce() if self.can_reduce else self

    @abc.abstractmethod
    def _reduce(self):
        return NotImplementedError()


class UnaryExpression(AST):
    def __init__(self, arg):
        """
        Constructor
        :param arg: arg
        """
        self.arg = arg


class BinaryExpression(AST):
    def __init__(self, left, op, right):
        """
        Constructor
        :param left: Left expression object
        :param op: operator as expression object
        :param right:  right expression object
        """
        self.left = left
        self.operator = op
        self.right = right