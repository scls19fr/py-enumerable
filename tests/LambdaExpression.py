from unittest import TestCase
from py_linq.queryable.expressions.unary import *
from py_linq.queryable.expressions.tree import ExpressionTree
from .TestModels import Student


class TestLambdaExpression(TestCase):
    def test_operators(self):
        of = OperatorFactory(Student)
        self.assertIsInstance(of.get_operator_expression("=="), EqualsExpression, "token should retrieve an instance of EqualsExpression")
        self.assertRaises(KeyError, of.get_operator_expression, "blah")

    def test_lambda_expression_tree(self):
        l = LambdaExpression(Student, "x => x.first_name == 'Bruce'")
        self.assertIsInstance(l.expression, ExpressionTree, "Expression property in LambdaExpression should be ExpressionTree instance")
        self.assertEquals(l.expression.length, 3, "Generated expression tree should be length of 3")
        self.assertIsInstance(l.expression.expression_at(0), PropertyExpression, "First expression in tree should be Property Expression")
        self.assertEquals(l.expression.expression_at(0).column_name, "first_name", "Column name should be first_name")
        self.assertIsInstance(l.expression.expression_at(1), OperatorExpression, "Second expression in tree should be Operator Expression")
        self.assertEquals(l.expression.expression_at(1).value, "==", "Second expression should be EqualsExpression")
        self.assertIsInstance(l.expression.expression_at(2), StringExpression, "Third Expression should be StringExpression")
        self.assertEquals(l.expression.expression_at(2).value, "Bruce", "Third expression should be Bruce")

    def test_invalid_expression(self):
        self.assertRaises(Exception, LambdaExpression, [Student, "x.first_name == \"Bruce\""])

    def test_and_expression(self):
        l = LambdaExpression(Student, "x => x.first_name == 'Bruce' and x.last_name == 'Fenske'")
        self.assertEquals(l.expression.length, 1, "Expression tree of conjuction statement is 1 node")
        self.assertIsInstance(l.expression.expression_at(0), AndExpressionTree, "Should be AndExpressionTree instance")
        l = LambdaExpression(Student, "x => x.first_name == 'Bruce' && x.last_name == 'Fenske'")
        self.assertEquals(l.expression.length, 1, "Expression tree of conjunction statement is 1 node")
        self.assertIsInstance(l.expression.expression_at(0), AndExpressionTree, "Should be AndExpressionTree instance")

    def test_or_expression(self):
        l = LambdaExpression(Student, "x => x.first_name == 'Bruce' or x.last_name == 'Fenske'")
        self.assertEquals(l.expression.length, 1, "Expression tree of disjunction statement is 1 node")
        self.assertIsInstance(l.expression.expression_at(0), OrExpressionTree, "Should be OrExpressionTree instance")

        l = LambdaExpression(Student, "x => x.first_name == 'Bruce' || x.last_name == 'Fenske'")
        self.assertEquals(l.expression.length, 1, "Expression tree of disjunction statement is 1 node")
        self.assertIsInstance(l.expression.expression_at(0), OrExpressionTree, "Should be OrExpressionTree instance")

    def test_and_or_expression(self):
        l = LambdaExpression(Student, "x => x.first_name == 'Bruce' and x.last_name == 'Fenske' or x.first_name == 'Dustin'")
        self.assertEquals(l.expression.length, 2, "Expression tree of conjunction and disjunction is 2 nodes - get {0}".format(l.expression.length))
        self.assertIsInstance(l.expression.expression_at(0), AndExpressionTree, "Should be AndExpressionTree instance")
        self.assertIsInstance(l.expression.expression_at(1), OrExpressionTree, "Should be OrExpressionTree instance - get {0}".format(l.expression.expression_at(1)))



