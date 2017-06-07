from . import UnaryExpression
from .processors import LambdaTokenProcessor
from .tree import ExpressionTree
from ... import Enumerable


class StringExpression(UnaryExpression):
    def __init__(self, T, arg):
        super(StringExpression, self).__init__(T, unicode(arg))


class FromExpression(StringExpression):
    def __init__(self, T):
        super(FromExpression, self).__init__(T, u"FROM")


class LambdaExpression(UnaryExpression):
    def __init__(self, T, lambda_string):
        super(LambdaExpression, self).__init__(T, lambda_string)
        self.__expression_tree = LambdaExpression.parse(T, lambda_string)

    @staticmethod
    def parse(T, s):
        '''
        Generates an expression tree by parsing expression string
        :param string: unicode string
        :return:
        '''
        et = ExpressionTree()
        s = unicode(s)
        if s is None or len(s) == 0 or "=>" not in s:
            raise Exception("LambdaExpression: invalid lambda string")
        lambda_split = s.split("=>")
        if len(lambda_split) != 2:
            raise Exception("LambdaExpression: invalid lambda string. Need a variable")
        variable = lambda_split[0].trim()
        tokens = Enumerable(lambda_split[1].split(' ').trim()).where(lambda x: x is not None and len(x) > 0).select(lambda x: x.trim())
        processor = LambdaTokenProcessor(variable)
        for t in tokens:
            processor.generate_expression(t)

