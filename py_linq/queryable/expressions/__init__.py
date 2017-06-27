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
        self._arg = arg
        super(UnaryExpression, self).__init__(T)

    @property
    def value(self):
        return self._arg


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


class SkipTakeExpression(AST):
    def __init__(self, T, limit=-1, offset=0):
        if not isinstance(limit, int):
            raise Exception(u"Limit argument {0} must be an integer".format(limit))
        if limit < -1:
            raise Exception(u"Limit argument must be at least -1")
        if not isinstance(offset, int):
            raise Exception(u"Offset argument must be an integer".format(offset))
        if offset < 0:
            raise Exception(u"Offset argument must be at least 0")
        self.limit = limit
        self.offset = offset
        super(SkipTakeExpression, self).__init__(T)

    def can_reduce(self, node):
        if isinstance(node, SkipTakeExpression):
            self.limit = max([self.limit, node.limit]) if self.limit < 0 else min([self.limit, node.limit])
            self.offset = self.offset + node.offset
            return True
        return False




