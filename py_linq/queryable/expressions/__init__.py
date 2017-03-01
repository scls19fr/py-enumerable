import abc


class ExpressionType(object):
    Constant = 0,
    Parameter = 1
    Lambda = 2


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


class Expression(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def can_reduce(self):
        raise NotImplementedError()

    @abc.abstractproperty
    def node_type(self):
        raise NotImplementedError()

    def accepts(self, expression_visitor):
        """
        Returns result of expression visitor visiting expression
        :param expression_visitor: An instance of expression visitor
        :return: expression instance
        """
        return expression_visitor.visit(self)

    @abc.abstractmethod
    def reduce(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def visit_children(self, expression_visitor):
        raise NotImplementedError()

    def __repr__(self):
        """
        Converts instance into string representation
        :return: string
        """
        klass = self.__class__.__name__
        private = "_{0}__".format(klass)
        args = []
        for name in self.__dict__:
            if name.startswith(private):
                value = self.__dict__[name]
                name = name[len(private):]
                args.append("{0}={1}".format(name, repr(value)))
        return "{0}({1})".format(klass, ", ".join(args))


