from . import AST


class ExpressionTree(object):
    """
    Data structure to store AST expressions and provide mechanisms for traversing, inserting, and deleting expressions
    """
    def __init__(self):
        self._expressions = []
        self._position = -1
        self._current = None

    def __len__(self):
        return self.length

    @property
    def current(self):
        """
        Returns the current AST subtree in the tree
        :return: AST expression
        """
        return self._current

    @property
    def length(self):
        return len(self._expressions)

    @property
    def position(self):
        return self._position

    @property
    def next(self):
        """
        Gets the next AST subtree in the tree
        :return: AST expression if next one exists, otherwise None
        """
        if self.length == 0 or self._position == self.length - 1:
            return None
        self._position += 1
        self._current = self._expressions[self._position]
        return self.current

    @property
    def peek(self):
        """
        Looks at the next AST substree in the tree
        :return: The next AST substree if one exists, otherwise None
        """
        if self.length == 0 or self._position == self.length - 1:
            return None
        return self._expressions[self._position + 1]

    def expression_at(self, i):
        self._position = i - 1
        return self.peek

    def __iter__(self):
        while self.next is not None:
            yield self.current
        self._position = -1

    def add_expression(self, expression):
        if not hasattr(expression, u"__class_type__"):
            return
        self._expressions.append(expression)

    def remove_expression(self, expression):
        self._expressions.remove(expression)


class ClauseExpressionTree(ExpressionTree):
    __class_type__ = None

    def __init__(self, T):
        self.__class_type__ = T
        super(ClauseExpressionTree, self).__init__()


class AndExpressionTree(ClauseExpressionTree):
    def __init__(self, T):
        super(AndExpressionTree, self).__init__(T)


class OrExpressionTree(ClauseExpressionTree):
    def __init__(self, T):
        super(OrExpressionTree, self).__init__(T)