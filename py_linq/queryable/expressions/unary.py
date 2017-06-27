from . import UnaryExpression
from .tree import ExpressionTree, AndExpressionTree, OrExpressionTree
from ... import Enumerable


class StringExpression(UnaryExpression):
    def __init__(self, T, arg):
        super(StringExpression, self).__init__(T, unicode(arg))


class FromExpression(StringExpression):
    def __init__(self, T):
        super(FromExpression, self).__init__(T, u"FROM")


class VariableExpression(StringExpression):
    def __init__(self, T, variable):
        super(VariableExpression, self).__init__(T, unicode(variable))


class PropertyExpression(StringExpression):
    def __init__(self, T, property):
        super(PropertyExpression, self).__init__(T, unicode(property))

    @property
    def column_name(self):
        column_member = Enumerable(self.__class_type__.get_column_members()).single_or_default(lambda c: c[0].lower() == self.value.lower())
        if column_member is None:
            raise KeyError(u"No such property found for {0} - {1}".format(self.__class_type__.name, self.value))
        column = column_member[1]
        return self.value if column.column_name is None or len(column.column_name) == 0 else column.column_name


class OperatorExpression(StringExpression):
    def __init__(self, T, op):
        super(OperatorExpression, self).__init__(T, op)


class EqualsExpression(OperatorExpression):
    def __init__(self, T):
        super(EqualsExpression, self).__init__(T, u"==")


class GreaterThanExpression(OperatorExpression):
    def __init__(self, T):
        super(GreaterThanExpression, self).__init__(T, u">")


class GreaterThanOrEqualExpression(OperatorExpression):
    def __init__(self, T):
        super(GreaterThanOrEqualExpression, self).__init__(T, u">=")


class LessThanExpression(OperatorExpression):
    def __init__(self, T):
        super(LessThanExpression, self).__init__(T, u"<")


class LessThanOrEqualExpression(OperatorExpression):
    def __init__(self, T):
        super(LessThanOrEqualExpression, self).__init__(T, u"<=")


class PlusExpression(OperatorExpression):
    def __init__(self, T):
        super(PlusExpression, self).__init__(T, u"+")


class MinusExpression(OperatorExpression):
    def __init__(self, T):
        super(MinusExpression, self).__init__(T, u"-")


class DivideExpression(OperatorExpression):
    def __init__(self, T):
        super(DivideExpression, self).__init__(T, u"/")


class MultiplicationExpression(OperatorExpression):
    def __init__(self, T):
        super(MultiplicationExpression, self).__init__(T, u"*")


class ModuloExpression(OperatorExpression):
    def __init__(self, T):
        super(ModuloExpression, self).__init__(T, u"%")


class OperatorFactory(object):
    def __init__(self, T):
        """
        Constructor
        :param T: underlying object type
        """
        self.object_type = T
        self.__token_expressions = {
            u"==": EqualsExpression(T),
            u">": GreaterThanExpression(T),
            u">=": GreaterThanOrEqualExpression(T),
            u"<": LessThanExpression(T),
            u"<=": LessThanOrEqualExpression(T),
            u"+": PlusExpression(T),
            u"-": MinusExpression(T),
            u"*": MultiplicationExpression(T),
            u"/": DivideExpression(T),
            u"%": ModuloExpression(T)
        }

    def has_token(self, token):
        return unicode(token) in self.__token_expressions.keys()

    def get_operator_expression(self, token):
        token = unicode(token)
        if not self.has_token(token):
            raise KeyError(u"No such operator token - {0}".format(token))
        return self.__token_expressions[token]


class LambdaExpression(StringExpression):
    def __init__(self, T, lambda_string):
        super(LambdaExpression, self).__init__(T, lambda_string)
        self.__expression_tree = LambdaExpression.parse(T, lambda_string)

    @property
    def expression(self):
        return self.__expression_tree

    @staticmethod
    def parse(T, s):
        """
        Generates an expression tree by parsing expression string
        :param string: unicode string
        :return:
        """
        et = ExpressionTree()
        s = unicode(s)
        if s is None or len(s) == 0 or "=>" not in s:
            raise Exception("LambdaExpression: invalid lambda string")
        lambda_split = s.split("=>")
        if len(lambda_split) != 2:
            raise Exception("LambdaExpression: invalid lambda string. Need a variable")

        variable = lambda_split[0].strip()
        tokens = Enumerable(lambda_split[1].split(' ')) \
            .where(lambda x: x is not None and len(x) > 0) \
            .select(lambda x: x.strip()).to_list()

        if u"and" in tokens or u"&&" in tokens:
            ands = lambda_split[1].split(u"and") if u"and" in tokens else []
            ands.extend(lambda_split[1].split(u"&&") if u"&&" in tokens else [])
            if len(ands) > 0:
                andTree = AndExpressionTree(T)
                for a in ands:
                    andTree.add_expression(LambdaExpression(T, u"{0} => {1}".format(variable, a)))
                et.add_expression(andTree)

        elif u"or" in tokens or u"||" in tokens:
            ors = lambda_split[1].split(u"or") if u"or" in tokens else []
            ors.extend(lambda_split[1].split(u"||") if u"||" in tokens else [])
            if len(ors) > 0:
                orTree = OrExpressionTree(T)
                for o in ors:
                    orTree.add_expression(LambdaExpression(T, u"{0} => {1}".format(variable, o)))
                et.add_expression(orTree)
        else:
            for t in tokens:
                expression = LambdaExpression.generate_expression(T, variable, t)
                et.add_expression(expression)
        return et

    @staticmethod
    def generate_expression(T, variable, token):
        """
        Attempts to generate an appropriate expression from a lambda string token
        :param variable: variable as string
        :param token: token as string
        :return: expression
        """""
        variable = u"{0}.".format(variable)
        if token.startswith(variable):
            return LambdaExpression.__generate_property_expression(T, variable, token)

        op = OperatorFactory(T)
        if op.has_token(token):
            return op.get_operator_expression(token)
        if token.startswith(u"'") or token.startswith("\\"""):
            char = token[0]
            return StringExpression(T, token.replace(char, ''))
        raise Exception(u"{0} not recognized".format(token))

    @staticmethod
    def __generate_property_expression(T, variable, token):
        token = unicode(token)
        return PropertyExpression(T, token[len(variable):])


