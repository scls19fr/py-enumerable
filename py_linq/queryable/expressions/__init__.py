import abc


class ExpressionType(object):
    Constant = 0
    Lambda = 1
    Add = 100
    Subtract = 101
    Multiply = 102
    Divide = 103


class ExpressionVisitor(object):

    def __init__(self):
        pass

    def visit(self, expression):
        """
        Visits the given expression node and returns new expression
        :param expression: an expression instance
        :return: another expression instance
        """
        if expression is None:
            return None

        expType = expression.node_type
        if expType == ExpressionType.Constant:
            return self.__visit_constant(expression)
        elif expType == ExpressionType.Lambda:
            return self.__visit_lambda(expression)
        else:
            raise TypeError("{0} is not a valid expression node type".format(expType))

    def __visit_constant(self, expression):
        return expression

    def __visit_lambda(self, expression):
        raise NotImplementedError()


class IExpression(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def can_reduce(self):
        raise NotImplementedError()

    @abc.abstractproperty
    def node_type(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def reduce(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def visit_children(self, expression_visitor):
        raise NotImplementedError()


class NaryExpression(IExpression):
    __metaclass__ = abc.ABCMeta

    def __init__(self, *args):
        """
        Constructor for NaryExpression
        :param args: list of expressions
        """
        self._children =[]
        for a in args:
            if not isinstance(a, IExpression):
                raise TypeError("all arguments should implement IExpression")
            self._children.append(a)

    @property
    def children(self):
        return self._children

    @abc.abstractproperty
    def node_type(self):
        raise NotImplementedError()

    @property
    def can_reduce(self):
        return len(self.children) > 0

    def reduce(self):
        if self.can_reduce:
            for i, c in enumerate(self.children):
                while c.can_reduce:
                    c = c.reduce()
                self.children[i] = c
        return self

    def visit_children(self, expression_visitor):
        for c in self.children:
            c = expression_visitor.visit(c)
        return self








