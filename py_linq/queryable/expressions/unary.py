import abc
from ..expressions import *


class UnaryExpression(Expression):
    __metaclass__ = abc.ABCMeta

    """
    Abstract implementation of Expression for unary operators
    """

    @property
    def can_reduce(self):
        return False

    @abc.abstractproperty
    def node_type(self):
        raise NotImplementedError()

    def reduce(self):
        return self

    def visit_children(self, expression_visitor):
        return self

    def __eq__(self, other):
        return self.node_type == other.node_type


class ConstantExpression(UnaryExpression):
    """
    Constant expression implementation
    """
    def __init__(self, value):
        self.__value = value

    @property
    def node_type(self):
        return ExpressionType.Constant

    @property
    def value(self):
        return self.__value

    def __eq__(self, other):
        return super(ConstantExpression, self).__eq__(other) and self.value == other.value

    def __add__(self, other):
        if super(ConstantExpression, self).__eq__(other):
            return ConstantExpression(self.value.__add__(other.value))
        raise TypeError("Incompatible type for addition: {0} and {1}".format(self.node_type, other.node_type))

    def __sub__(self, other):
        if super(ConstantExpression, self).__eq__(other):
            return ConstantExpression(self.value.__sub__(other.value))
        raise TypeError("Incompatible type for subtraction: {0} and {1}".format(self.node_type, other.node_type))

    def __mul__(self, other):
        if super(ConstantExpression, self).__eq__(other):
            return ConstantExpression(self.value.__mul__(other.value))
        raise TypeError("Incompatible type for multiplicaton: {0} and {1}".format(self.node_type, other.node_type))

    def __div__(self, other):
        if super(ConstantExpression, self).__eq__(other):
            return ConstantExpression(self.value.__div__(other.value))
        raise TypeError("Incompatible type for division: {0} and {1}".format(self.node_type, other.node_type))


class LambdaExpression(UnaryExpression):
    """
    Lambda expression implementation
    """

    def __init__(self, func):
        self.__func = func

    @property
    def node_type(self):
        return ExpressionType.Lambda

    @property
    def body(self):
        """
        Return bytecode of lambda expression
        :return: string instance
        """
        return self.__func.func_code.co_code

    def compile(self, arg):
        """
        Executes the code in lambda expression with given argument
        :param arg: object
        :return: result of code execution
        """
        return self.__func.__call__(arg)

    def __eq__(self, other):
        return super(LambdaExpression, self).__eq__(other) and self.body == other.body

    def __add__(self, other):
        raise NotImplementedError("Nonsensical to add 2 lambda expressions")

    def __sub__(self, other):
        raise NotImplementedError("Nonsensical to subtract 2 lambda expressions")

    def __mul__(self, other):
        raise NotImplementedError("Nonsensical to multiply 2 lambda expressions")

    def __div__(self, other):
        raise NotImplementedError("Nonsensical to divide 2 lambda expressions")
