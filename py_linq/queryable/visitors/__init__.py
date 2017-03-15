import abc


class IExpressionVisitor(object):
    @abc.abstractmethod
    def visit(self, expression):
        raise NotImplementedError()

