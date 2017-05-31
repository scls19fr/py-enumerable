from . import BinaryExpression, SelectExpression
from .unary import *


class TableExpression(BinaryExpression):
    def __init__(self, model):
        left = SelectExpression(model)
        op = StringExpression("FROM")
        right = StringExpression(model.__table_name__)
        super(TableExpression, self).__init__(left, op, right)






