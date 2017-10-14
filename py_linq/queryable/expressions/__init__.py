import abc
import meta
import ast
from ..visitors.lambda_visitors import SqlLambdaTranslator


class Expression(object):
    __class_type__ = None

    def __init__(self, T):
        if not hasattr(T, u"__table_name__"):
            raise AttributeError(u"{0} does not appear to be derived from Model".format(T.__class__.__name__))
        self.__class_type__ = T

    @property
    def type(self):
        return self.__class_type__

    @abc.abstractmethod
    def visit(self, visitor):
        raise NotImplementedError()


class UnaryExpression(Expression):

    def __init__(self, T, op_exp, exp):
        super(UnaryExpression, self).__init__(T)
        self.op = op_exp
        self.exp = exp

    def visit(self, visitor):
        return visitor.visit_UnaryExpression(self)

    def __repr__(self):
        return u"{0}(op={1}, exp={2})".format(self.__class__.__name__, self.op.__repr__(), self.exp.__repr__())


class SelectExpression(Expression):

    def __init__(self, T, func):
        super(SelectExpression, self).__init__(T)
        self.func = func

    def visit(self, visitor):
        return visitor.visit_SelectExpression(self)

    def __repr__(self):
        t = LambdaExpression.parse(self.type, self.func)
        return u"Select(func={0})".format(ast.dump(t))


class TableExpression(Expression):

    def __init__(self, T):
        super(TableExpression, self).__init__(T)

    def visit(self, visitor):
        return visitor.visit_TableExpression(self)

    def __repr__(self):
        return u"Table(table_name={0})".format(self.type.table_name)


class LambdaExpression(object):

    """
    Parses a python lambda expression and returns a modified tree that contains
    appropriate sql syntax
    """
    @staticmethod
    def parse(T, func):
        tree = meta.decompiler.decompile_func(func)
        translator = SqlLambdaTranslator(T)
        translator.generic_visit(tree)
        return tree
