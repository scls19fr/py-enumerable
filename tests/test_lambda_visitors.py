import meta
import ast
from unittest import TestCase
from py_linq.queryable.visitors.lambda_visitors import SqlLambdaTranslator
from .models import Student


class SqlLambdaTranslatorTest(TestCase):
    def setUp(self):
        self.simple_eq_uni = lambda x: x.first_name == u"Bruce"
        self.simple_eq_str = lambda x: x.first_name == 'Bruce'
        self.simple_lte = lambda x: x.gpa <= 10
        self.simple_lt = lambda x: x.gpa < 10
        self.simple_gte = lambda x: x.gpa >= 10
        self.simple_gt = lambda x: x.gpa > 10
        self.simple_plus = lambda x: x.gpa + 10
        self.simple_minus = lambda x: x.gpa - 10
        self.simple_div = lambda x: x.gpa / 10
        self.simple_mult = lambda x: x.gpa * 10
        self.simple_mod = lambda x: x.gpa % 2
        self.simple_and = lambda x: x.gpa >= 10 and x.gpa <= 50
        self.simple_or = lambda x: x.gpa >= 10 or x.first_name == u'Bruce'

    @staticmethod
    def translate(func):
        tree = meta.decompiler.decompile_func(func)
        translator = SqlLambdaTranslator(Student)
        translator.generic_visit(tree)
        return tree

    def test_Eq(self):
        t = SqlLambdaTranslatorTest.translate(self.simple_eq_uni)
        self.assertIsInstance(t.body.ops[0], ast.Eq, u"Should be Eq instance")
        self.assertEquals(t.body.ops[0].sql, u"=", u"Eq() node should have sql property of '='")

    def test_LtE(self):
        t = SqlLambdaTranslatorTest.translate(self.simple_lte)
        self.assertIsInstance(t.body.ops[0], ast.LtE, u"Should be LtE instance")
        self.assertEquals(t.body.ops[0].sql, u"<=", u"LtE() node should have sql property of '<=")

    def test_Lt(self):
        t = SqlLambdaTranslatorTest.translate(self.simple_lt)
        self.assertIsInstance(t.body.ops[0], ast.Lt, u"Should be Lt instance")
        self.assertEquals(t.body.ops[0].sql, u"<", u"Lt() node should have sql property of '<'")

    def test_GtE(self):
        t = SqlLambdaTranslatorTest.translate(self.simple_gte)
        self.assertIsInstance(t.body.ops[0], ast.GtE, u"Should be GtE instance")
        self.assertEquals(t.body.ops[0].sql, u">=", u"GtE() node should have sql property of '>='")

    def test_Gt(self):
        t = SqlLambdaTranslatorTest.translate(self.simple_gt)
        self.assertIsInstance(t.body.ops[0], ast.Gt, u"Should be Gt instance")
        self.assertEquals(t.body.ops[0].sql, u">", u"Gt() node should have sql property of '>")

    def test_plus(self):
        t = SqlLambdaTranslatorTest.translate(self.simple_plus)
        self.assertIsInstance(t.body.op, ast.Add, u"Should be Add instance")
        self.assertEquals(t.body.op.sql, u"+", u"Add() node should have sql property of '+'")

    def test_minus(self):
        t = SqlLambdaTranslatorTest.translate(self.simple_minus)
        self.assertIsInstance(t.body.op, ast.Sub, u"Should be Sub instance")
        self.assertEquals(t.body.op.sql, u"-", u"Sub() node should have sql property of '-'")

    def test_div(self):
        t = SqlLambdaTranslatorTest.translate(self.simple_div)
        self.assertIsInstance(t.body.op, ast.Div, u"Should be Div instance")
        self.assertEquals(t.body.op.sql, u"/", u"Div() node should have sql property of '/'")

    def test_mult(self):
        t = SqlLambdaTranslatorTest.translate(self.simple_mult)
        self.assertIsInstance(t.body.op, ast.Mult, u"Should be Mult instance")
        self.assertEquals(t.body.op.sql, u"*", u"Mult() node should have sql property of '*'")

    def test_mod(self):
        t = SqlLambdaTranslatorTest.translate(self.simple_mod)
        self.assertIsInstance(t.body.op, ast.Mod, u"Should be Mod instance")
        self.assertEquals(t.body.op.sql, u"%", u"Mod() node should have sql property of '%")

    def test_num_binop(self):
        t = SqlLambdaTranslatorTest.translate(self.simple_mult)
        self.assertIsInstance(t.body.right, ast.Num, u"Should be a Num instance")
        self.assertEquals(
            t.body.right.sql,
            unicode(t.body.right.n),
            u"Num() node should have sql property equal to {0}".format(t.body.right.n)
        )

    def test_num_compare(self):
        t = SqlLambdaTranslatorTest.translate(self.simple_gte)
        self.assertIsInstance(t.body.comparators[0], ast.Num, u"Should be a Num instance")
        self.assertEquals(
            t.body.comparators[0].sql,
            unicode(t.body.comparators[0].n),
            u"Num() node should have sql property equal to {0}".format(t.body.comparators[0].n)
        )

    def test_str(self):
        t = SqlLambdaTranslatorTest.translate(self.simple_eq_str)
        self.assertIsInstance(t.body.comparators[0], ast.Str, u"Should be a Str instance")
        self.assertEquals(
            t.body.comparators[0].sql,
            unicode(t.body.comparators[0].s),
            u"Str() node should have sql property equal to {0}".format(t.body.comparators[0].sql)
        )

    def test_attribute(self):
        t = SqlLambdaTranslatorTest.translate(self.simple_eq_uni)
        self.assertIsInstance(t.body.left, ast.Attribute, u"Should be Attribute instance")
        self.assertEquals(
            t.body.left.sql,
            Student.first_name.column_name,
            u"{0} should equal {1}".format(t.body.left.sql, Student.first_name.column_name)
        )

    def test_and(self):
        t = SqlLambdaTranslatorTest.translate(self.simple_and)
        self.assertIsInstance(t.body.op, ast.And, u"Should be And instance")
        self.assertEquals(
            t.body.op.sql,
            u"AND",
            u"And() node should have sql property equal 'AND'"
        )

    def test_or(self):
        t = SqlLambdaTranslatorTest.translate(self.simple_or)
        self.assertIsInstance(t.body.op, ast.Or, u"Should be Or instance")
        self.assertEquals(
            t.body.op.sql,
            u"OR",
            u"Or() node should have sql property equal 'Or'"
        )

    def test_compare_simple(self):
        t = SqlLambdaTranslatorTest.translate(self.simple_lte)
        correct = u"gpa <= 10"
        self.assertIsInstance(t.body, ast.Compare, u"Should be a Compare instance")
        self.assertEquals(
            t.body.sql,
            correct,
            u"{0} should be same as {1}".format(t.body.sql, correct)
        )

    def test_compare_complex(self):
        t = SqlLambdaTranslatorTest.translate(self.simple_and)
        values = t.body.values
        corrects = [u"gpa >= 10", u"gpa <= 50"]
        for i in range(0, len(values) - 1, 1):
            correct = corrects[i]
            value = values[i].sql
            self.assertEquals(value, correct, u"{0} should equal {1}".format(value, correct))

    def test_boolop(self):
        t = SqlLambdaTranslatorTest.translate(self.simple_and)
        correct = u"gpa >= 10 AND gpa <= 50"
        self.assertIsInstance(t.body, ast.BoolOp, u"Should be a BoolOp instance")
        self.assertEqual(
            t.body.sql,
            correct,
            u"{0} should equal {1}".format(t.body.sql, correct)
        )

    def test_binop(self):
        t = SqlLambdaTranslatorTest.translate(self.simple_plus)
        correct = u"gpa + 10"
        self.assertIsInstance(t.body, ast.BinOp, u"Should be a BinOp instance")
        self.assertEqual(
            t.body.sql,
            correct,
            u"{0} should equal {1}".format(t.body.sql, correct)
        )









