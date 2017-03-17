import abc


class IExpression(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def can_reduce(self):
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
            if a is not None and not isinstance(a, IExpression):
                raise TypeError("all arguments should implement IExpression")
            self._children.append(a)

    @property
    def children(self):
        return self._children

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
        for i, c in enumerate(self.children):
            c = expression_visitor.visit(c)
            self.children[i] = c
        return self








