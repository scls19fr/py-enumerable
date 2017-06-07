
class LambdaTokenProcessor(object):
    __class_type__ = None
    __operatorTokens = ['&&', 'and', '||', 'or', '==', '*', '+', '-', '/', '<=', '<', '>', '>=']

    def __init__(self, T, variable):
        self.__class_type__ = T
        self.__variable = variable

    def generate_expression(self, token):
        '''
        Attempts to generate an appropriate expression from a lambda string token
        :param variable: variable as string
        :param token: token as string
        :return: expression
        '''
        if token in self.__operatorTokens.keys():
            return self.__generate_operator_expression(token)
        raise NotImplementedError()

    def __generate_operator_expression(self, token):
        raise NotImplementedError()


