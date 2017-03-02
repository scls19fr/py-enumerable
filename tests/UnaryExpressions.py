from unittest import TestCase
from py_linq.queryable.expressions.unary import ConstantExpression, LambdaExpression


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

    def testAdd(self):
        added = self.constantInt + self.constantInt2
        self.assertEqual(added.value, 10, "addition of constantInt and constantInt2 equals 10")
        self.assertRaises(TypeError, self.constantInt + self.constantString, "TypeError should be raised when trying to add two different node types")

    def testSubtract(self):
        subtracted = self.constantInt - self.constantInt2
        self.assertEqual(subtracted.value, 0, "subtraction of constantInt2 from constantInt equals 0")
        self.assertRaises(TypeError,self.constantInt - self.constantString, "TypeError should be raised when trying to subtract two different node types")




class TestLambdaExpression(TestCase):
    def setUp(self):
        self.addLambda = LambdaExpression(lambda x: x + 2)
        self.addLambda2 = LambdaExpression(lambda y: y + 2)
        self.boolLambda = LambdaExpression(lambda x: x <= 2)

    def testBody(self):
        self.assertEqual(self.addLambda, self.addLambda2, "addLambda and addLambda 2 should equal")
        self.assertNotEqual(self.addLambda, self.boolLambda, "addLambda and boolLambda should not equal")

    def testCompile(self):
        self.assertEqual(self.addLambda.compile(2), 4, "Executing addLambda with arg=2 should equal 4")
        self.assertTrue(self.boolLambda.compile(2), "boolLambda list should return true")
