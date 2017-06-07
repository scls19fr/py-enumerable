from . import AST


class ExpressionTree(object):
    """
    Data structure to store AST expressions and provide mechanisms for traversing, inserting, and deleting expressions
    """
    def __init__(self):
        self.__expressions = []
        self.__position = -1
        self.__current = None

    def __len__(self):
        return self.length

    @property
    def current(self):
        """
        Returns the current AST subtree in the tree
        :return: AST expression
        """
        return self.__current

    @property
    def length(self):
        return len(self.__expressions)

    @property
    def position(self):
        return self.__position

    @property
    def next(self):
        """
        Gets the next AST subtree in the tree
        :return: AST expression if next one exists, otherwise None
        """
        if self.length == 0 or self.__position == self.length - 1:
            return None
        self.__position += 1
        self.__current = self.__expressions[self.__position]
        return self.current

    @property
    def peek(self):
        """
        Looks at the next AST substree in the tree
        :return: The next AST substree if one exists, otherwise None
        """
        if self.length == 0 or self.__position == self.length - 1:
            return None
        return self.__expressions[self.__position + 1]

    def expression_at(self, i):
        self.__position = i - 1
        return self.peek

    def __iter__(self):
        while self.next is not None:
            yield self.current
        self.__position = -1

    def add_expression(self, expression):
        if not isinstance(expression, AST):
            return
        self.__expressions.append(expression)

    def remove_expression(self, expression):
        self.__expressions.remove(expression)
