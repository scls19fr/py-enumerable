from unittest import TestCase
from datetime import datetime
from py_linq.queryable.expressions.unary import ConstantExpression
from py_linq.queryable.expressions.binary import AddExpression, SubstractExpression, MultiplyExpression, DivideExpression


class TestBinaryExpression(TestCase):
    def setUp(self):
        self.addExpression = AddExpression(ConstantExpression(5), ConstantExpression(14))
        self.subtractExpression = SubstractExpression(ConstantExpression(datetime(2017, 2, 28)), ConstantExpression(datetime(2017, 2, 1)))
        self.multiplyExpression = MultiplyExpression(ConstantExpression(5), ConstantExpression(-2))
        self.divideExpression = DivideExpression(ConstantExpression(float(1.00)), ConstantExpression(0.20))

    def testReduce(self):
        add_reduced = self.addExpression.reduce() if self.addExpression.can_reduce else self.addExpression
        self.assertIsInstance(add_reduced, ConstantExpression, "Reduced form of addExpression with ConstantExpression args should be ConstantExpression")
        self.assertEqual(add_reduced.value, 19, "Sum of 5 and 14 is 19")

        subtract_reduced = self.subtractExpression.reduce() if self.subtractExpression.can_reduce else self.subtractExpression
        self.assertIsInstance(subtract_reduced, ConstantExpression, "Reduced form of substractExpression with ConstantExpression args should be ConstantExpression")
        self.assertEqual(subtract_reduced.value, datetime(2017, 2, 28) - datetime(2017, 2, 1), "Does not equal timespan")

        mul_reduced = self.multiplyExpression.reduce() if self.multiplyExpression.can_reduce else self.multiplyExpression
        self.assertIsInstance(mul_reduced, ConstantExpression, "Reduced form of mulitplyExpression with ConstantExpression args should be ConstantExpression")
        self.assertEqual(mul_reduced.value, -10, "5 * -2 = -10")

        div_reduced = self.divideExpression.reduce() if self.divideExpression.can_reduce else self.divideExpression
        self.assertIsInstance(div_reduced, ConstantExpression, "Reduced form of divideExpression with ConstantExpression args should be ConstantExpression")
        self.assertEqual(div_reduced.value, float(5), "1.00 / 0.20 = 5.00")

