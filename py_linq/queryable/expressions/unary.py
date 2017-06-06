from . import UnaryExpression


class StringExpression(UnaryExpression):
    def __init__(self, T, arg):
        super(StringExpression, self).__init__(T, unicode(arg))


class TakeExpression(UnaryExpression):
    def __init__(self, T, limit):
        if not isinstance(limit, int):
            raise Exception(u"Limit argument {0} must be an integer".format(limit))
        super(TakeExpression, self).__init__(T, limit)
