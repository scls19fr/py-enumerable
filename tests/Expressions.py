from unittest import TestCase
from py_linq.queryable.expressions.ConstantExpression import ConstantExpression
from py_linq.queryable.expressions.LambdaExpression import LambdaExpression


class TestConstantExpression(TestCase):
    def setUp(self):
        self.constantInt = ConstantExpression(5)
        self.constantInt2 = ConstantExpression(5)
        self.constantString = ConstantExpression(u"hello")

    def testValue(self):
        self.assertEqual(self.constantInt.value, 5, "constantInt value should be 5")
        self.assertEqual(self.constantString.value, u"hello", "constantString value should be 'hello'")
        self.assertIsInstance(self.constantInt.value, int, "constantInt value should be of type int")
        self.assertIsInstance(self.constantString.value, unicode, "constantString value should be of type unicode")

    def testEqual(self):
        self.assertEqual(self.constantInt, self.constantInt2, "constantInt and constantInt2 are equal")
        self.assertNotEqual(self.constantInt, self.constantString, "constantInt and constantString should not be equal")


class TestLambdaExpression(TestCase):
    def setUp(self):
        self.addLambda = LambdaExpression(lambda x: x + 2)
        self.boolLambda = LambdaExpression(lambda x: x <= 2)

    def testCompile(self):
        self.assertEqual(self.addLambda.compile(2), 4, "Executing addLambda with arg=2 should equal 4")
        self.assertTrue(self.boolLambda.compile(2), "boolLambda list should return true")
