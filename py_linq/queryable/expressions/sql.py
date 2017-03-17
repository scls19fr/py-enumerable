from ..expressions.binary import BinaryExpression
from ..expressions.unary import ConstantExpression


class SelectExpression(BinaryExpression):
    def __init__(self, model_expression, lambda_expression=None):
        super(SelectExpression, self).__init__(model_expression, lambda_expression)

    @property
    def can_reduce(self):
        return True

    def reduce(self):
        """
        Reduce select expression into select string constant expression
        :return: ConstantExpression as tuple of sql column names
        """
        desired_columns = [col.column_name for col in self.right.compile(self.left.model)] if self.right is not None else [col[1].column_name for col in self.left.model.get_column_members()]
        column_members = [(name, col) for name, col in self.left.model.get_column_members() if col.column_name in desired_columns]

        return ConstantExpression(tuple(["{0} as {1}".format(col.column_name, name) for name, col in column_members]))


class WhereExpression(BinaryExpression):
    def __init__(self, lambda_expression, model_expression):
        super(WhereExpression, self).__init__(lambda_expression, model_expression)

    @property
    def can_reduce(self):
        return True

    def reduce(self):
        """
        Reduce where expression into
        :return:
        """
        raise NotImplementedError()