class AST(object):
    __class_type__ = None

    def __init__(self, T):
        """
        This is my hack for generics so that we can keep track of the underlying model in the AST
        :param T: object type. Similar to generics
        """
        self.__class_type__ = T

    def can_reduce(self, node):
        return False

    def visit(self, visitor):
        return visitor.visit(self)


class UnaryExpression(AST):
    def __init__(self, T, arg):
        """
        Constructor
        :param arg: arg
        """
        self.__arg = arg
        super(UnaryExpression, self).__init__(T)

    @property
    def value(self):
        return self.__arg


class BinaryExpression(AST):
    def __init__(self, T, left, op, right):
        """
        Constructor
        :param left: Left expression object
        :param op: operator as expression object
        :param right:  right expression object
        """
        self.left = left
        self.operator = op
        self.right = right
        super(BinaryExpression, self).__init__(T)


class SelectExpression(AST):
    def __init__(self, T, func=None):
        self.func = func
        super(SelectExpression, self).__init__(T)


class CountExpression(AST):
    def __init__(self, T):
        super(CountExpression, self).__init__(T)



