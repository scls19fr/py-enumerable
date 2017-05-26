from ..expressions import UnaryExpression


class StringExpression(UnaryExpression):
    def __init__(self, arg):
        super(StringExpression, self).__init__(arg)


class FromExpression(StringExpression):
    def __init__(self):
        super(FromExpression, self).__init__("FROM")


class ModelExpression(UnaryExpression):
    def __init__(self, model):
        """
        Constructor
        :param model: A py-linq entity model
        """
        super(ModelExpression, self).__init__(model)

    @property
    def model (self):
        return self.arg

