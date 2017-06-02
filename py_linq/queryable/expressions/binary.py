from . import BinaryExpression, SelectExpression
from .unary import *


class TableExpression(BinaryExpression):
    def __init__(self, model):
        left = SelectExpression(model)
        op = StringExpression(model, "FROM")
        right = StringExpression(model, model.__table_name__)
        super(TableExpression, self).__init__(model, left, op, right)






