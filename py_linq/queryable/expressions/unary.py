from . import UnaryExpression


class StringExpression(UnaryExpression):
    def __init__(self, T, arg):
        super(StringExpression, self).__init__(T, arg)

