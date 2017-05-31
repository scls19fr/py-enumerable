
class AST(object):
    def visit(self, visitor):
        return visitor.visit(self)


class UnaryExpression(AST):
    def __init__(self, arg):
        """
        Constructor
        :param arg: arg
        """
        self.__arg = arg

    @property
    def value(self):
        return self.__arg


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


class SelectExpression(AST):
    def __init__(self, model, func=None):
        self.func = func
        self.model = model
