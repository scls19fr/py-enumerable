import abc
import meta
import ast
from ..visitors.lambda_visitors import SqlLambdaTranslator


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


class Expression(object):
    __class_type__ = None

    def __init__(self, T):
        if not hasattr(T, u"__table_name__"):
            raise AttributeError(u"{0} does not appear to be derived from Model".format(T.__class__.__name__))
        self.__class_type__ = T
        self.visited = False

    def __eq__(self, other):
        return self.type == other.type and self.__repr__() == other.__repr__()

    @property
    def type(self):
        return self.__class_type__

    @abc.abstractmethod
    def visit(self, visitor):
        raise NotImplementedError()

    @abc.abstractproperty
    def children(self):
        raise NotImplementedError()

    def find(self, expression):
        """
        Finds first matching expression using breadth first search
        :param expression: An expression type
        :return: First expression that matches given expression else None
        """
        q = self.children
        while len(q) > 0:
            node = q[0]
            if type(node) == expression:
                return node
            for n in node.children:
                q.append(n)
            q.pop(0)
        return None


class UnaryExpression(Expression):

    def __init__(self, T, op_exp, exp):
        super(UnaryExpression, self).__init__(T)
        self.op = op_exp
        self.exp = exp

    def visit(self, visitor):
        return visitor.visit_UnaryExpression(self)

    @property
    def children(self):
        return [self.op, self.exp]

    def __repr__(self):
        return u"{0}(op={1}, exp={2})".format(self.__class__.__name__, self.op.__repr__(), self.exp.__repr__())


class SelectExpression(Expression):

    def __init__(self, T, func=None):
        super(SelectExpression, self).__init__(T)
        self.func = func

    def visit(self, visitor):
        return visitor.visit_SelectExpression(self)

    @property
    def children(self):
        return []

    def __repr__(self):
        t = LambdaExpression.parse(self.type, self.func)
        return u"Select(func={0})".format(ast.dump(t))


class TableExpression(Expression):

    def __init__(self, T):
        super(TableExpression, self).__init__(T)

    def visit(self, visitor):
        return visitor.visit_TableExpression(self)

    @property
    def children(self):
        return []

    def __repr__(self):
        return u"Table(table_name={0})".format(self.type.table_name)


class WhereExpression(Expression):

    def __init__(self, T, func):
        super(WhereExpression, self).__init__(T)
        if func is None:
            raise Exception(u"WhereExpression must have lambda expression constructor parameter")
        self.func = func

    def visit(self, visitor):
        return visitor.visit_WhereExpression(self)

    @property
    def children(self):
        return []

    def __repr__(self):
        return u"Where(func={0})".format(ast.dump(LambdaExpression.parse(self.type, self.func)))


class CountExpression(Expression):

    def __init__(self, T):
        super(CountExpression, self).__init__(T)

    def visit(self, visitor):
        return visitor.visit_CountExpression(self)

    @property
    def children(self):
        return []

    def __repr__(self):
        return u"Count()"


class CountUnaryExpression(UnaryExpression):
    def __init__(self, T, exp):
        super(CountUnaryExpression, self).__init__(T, CountExpression(T), exp)

    def visit(self, visitor):
        return visitor.visit_CountUnaryExpression(self)


class TakeExpression(Expression):

    def __init__(self, T, limit):
        super(TakeExpression, self).__init__(T)
        self.limit = limit

    def visit(self, visitor):
        return visitor.visit_TakeExpression(self)

    @property
    def children(self):
        return []

    def __repr__(self):
        return u"Take(limit={0})".format(self.limit)


class TakeUnaryExpression(UnaryExpression):

    def __init__(self, T, exp, limit):
        super(TakeUnaryExpression, self).__init__(T, TakeExpression(T, limit), exp)

    def visit(self, visitor):
        return visitor.visit_TakeUnaryExpression(self)


class SkipExpression(Expression):

    def __init__(self, T, skip):
        super(SkipExpression, self).__init__(T)
        self.skip = skip

    def visit(self, visitor):
        return visitor.visit_SkipExpression(self)

    @property
    def children(self):
        return []

    def __repr__(self):
        return u"Skip(skip={0}".format(self.skip)


class SkipUnaryExpression(UnaryExpression):

    def __init__(self, T, exp, skip):
        super(SkipUnaryExpression, self).__init__(T, SkipExpression(T, skip), exp)

    def visit(self, visitor):
        return visitor.visit_SkipUnaryExpression(self)

