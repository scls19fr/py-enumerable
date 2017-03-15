from ..expressions import ExpressionType
from ..expressions.binary import BinaryExpression
from ..expressions.unary import ConstantExpression


class SelectExpression(BinaryExpression):
    def __init__(self, lambda_expression, model_expression):
        super(SelectExpression, self).__init__(lambda_expression, model_expression)

    @property
    def can_reduce(self):
        return True

    def node_type(self):
        return ExpressionType.SelectExpression

    def reduce(self):
        """
        Reduce select expression into select string constant expression
        :return: ConstantExpression as tuple of sql column names
        """
        return ConstantExpression(col.column_name for col in self.left.compile(self.right.model))





