import abc


class IExpressionVisitor(object):

    @abc.abstractmethod
    def visit_UnaryExpression(self, expression):
        raise NotImplementedError()

    @abc.abstractmethod
    def visit_SelectExpression(self, expression):
        raise NotImplementedError()

    @abc.abstractmethod
    def visit_TableExpression(self, expression):
        raise NotImplementedError()




