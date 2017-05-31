from . import UnaryExpression


class StringExpression(UnaryExpression):
    def __init__(self, arg):
        super(StringExpression, self).__init__(arg)

