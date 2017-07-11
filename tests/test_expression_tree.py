from unittest import TestCase
from py_linq.queryable.expressions.tree import ExpressionTree
from py_linq.queryable.expressions import *
from py_linq.queryable.expressions.unary import StringExpression
from py_linq.queryable.expressions.binary import TableExpression
from .models import Student

class ExpressionTreeTest(TestCase):
    def setUp(self):
        self.expression_tree = ExpressionTree()

    def test_add(self):
        self.expression_tree.add_expression("SHOULDN'T ADD")
        self.assertEquals(self.expression_tree.length, 0, "Expression tree shouldn't contain any expressions")

        self.expression_tree.add_expression(TableExpression(Student))
        self.assertEquals(self.expression_tree.length, 1, "Expression tree should have one expression in it")

    def test_remove(self):
        expression = TableExpression(Student)
        self.expression_tree.add_expression(expression)
        self.assertEquals(self.expression_tree.length, 1)

        self.expression_tree.remove_expression(expression)
        self.assertEquals(self.expression_tree.length, 0, "Expression tree shouldn't contain any expressions after removal")

    def test_next(self):
        self.assertIsNone(self.expression_tree.next, "Expression tree should be empty, so next should return None")
        self.assertEquals(self.expression_tree.position, -1, "Position should be -1")
        self.expression_tree.add_expression(TableExpression(Student))

        first_expression = self.expression_tree.peek
        self.assertIsNotNone(first_expression, "Peeking at next expression should not be none")
        self.assertIsInstance(first_expression, TableExpression)
        self.assertEquals(self.expression_tree.position, -1, "Still haven't moved position, should still be -1")

        first_expression = self.expression_tree.next
        self.assertIsNotNone(first_expression, "First expression should not be none")
        self.assertIsInstance(first_expression, TableExpression)
        self.assertEquals(self.expression_tree.position, 0, "Position should be 0")
        self.assertIsNone(self.expression_tree.peek, "Peeking at next expression should give None")
        self.assertIsNone(self.expression_tree.next, "Expression tree shouldn't contain any more expressions, so next should give None")

    def tearDown(self):
        self.expression_tree = None