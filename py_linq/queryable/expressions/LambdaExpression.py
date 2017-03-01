from ..expressions import Expression, ExpressionType


class LambdaExpression(Expression):
    """
    Lambda expression implementation
    """

    def __init__(self, func):
        self.__func = func

    @property
    def can_reduce(self):
        return False

    @property
    def node_type(self):
        return ExpressionType.Lambda

    @property
    def body(self):
        """
        Return bytestring of lambda expression
        :return: bytestring instance
        """
        return self.__func.func_code.co_code

    def reduce(self):
        return self

    def visit_children(self, expression_visitor):
        return self

    def compile(self, arg):
        """
        Executes the code in lambda expression with given argument
        :param arg: object
        :return: result of code execution
        """
        return self.__func.__call__(arg)

    def __eq__(self, other):
        return self.body == other.body
