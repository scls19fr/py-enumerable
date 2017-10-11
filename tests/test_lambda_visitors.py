import meta
import ast
from unittest import TestCase
from py_linq.queryable.visitors.lambda_visitors import SqlLambdaTranslator


class SqlLambdaTranslatorTest(TestCase):
    def setUp(self):
        self.simple_eq_uni = lambda x: x.first_name == u"Bruce"
        self.simple_eq_str = lambda x: x.first_name == 'Bruce'
        self.simple_lte = lambda x: x.amount <= 10
        self.simple_lt = lambda x: x.amount < 10
        self.simple_gte = lambda x: x.amount >= 10
        self.simple_gt = lambda x: x.amount > 10
        self.simple_plus = lambda x: x.amount + 10
        self.simple_minus = lambda x: x.amount - 10
        self.simple_div = lambda x: x.amount / 10
        self.simple_mult = lambda x: x.amount * 10

    @staticmethod
    def translate(func):
        tree = meta.decompiler.decompile_func(func)
        translator = SqlLambdaTranslator()
        translator.generic_visit(tree)
        return tree

    def test_Eq(self):
        t = SqlLambdaTranslatorTest.translate(self.simple_eq_uni)
        self.assertIsInstance(t.body.ops[0], ast.Eq, u"Should be Eq instance")
        self.assertEquals(t.body.ops[0].sql, u"=", u"Eq() node should have sql property of '='")
        print ast.dump(t)

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

    # def test_unicode(self):
    #     t = SqlLambdaTranslatorTest.translate(self.simple_eq_uni)
    #     self.assertIsInstance(t.body.comparators[0], unicode, u"Should be a unicode instance")
    #     self.assertEquals(
    #         t.body.comparators[0].sql,
    #         t.body.comparators,
    #         u"unicode node should have sql property equal to {0}".format(t.body.comparators[0].sql)
    #     )


