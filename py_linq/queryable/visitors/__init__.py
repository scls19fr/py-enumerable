import abc


class IExpressionVisitor(object):
    def __init__(self):
        super(IExpressionVisitor, self).__init__()

    @abc.abstractmethod
    def visit(self, expression):
        raise NotImplementedError()




