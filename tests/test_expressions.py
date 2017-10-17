from unittest import TestCase
from py_linq.queryable.expressions import *
from py_linq.queryable.visitors.sql import SqlVisitor
from .models import Student


class TestSqlExpressions(TestCase):

    def setUp(self):
        self.visitor = SqlVisitor()
        self.table_expression = TableExpression(Student)

    def test_select_expression(self):
        se = UnaryExpression(Student, SelectExpression(Student, lambda x: x.first_name), self.table_expression)
        sql = self.visitor.visit(se)
        correct = u"SELECT student.first_name AS first_name FROM student"
        self.assertEqual(
            sql,
            correct,
            u"{0} does not equal {1}".format(sql, correct)
        )

    def test_select_all(self):
        se = UnaryExpression(Student, SelectExpression(Student), self.table_expression)
        sql = self.visitor.visit(se)
        self.assertTrue(sql.startswith(u"SELECT"))
        self.assertTrue(sql.endswith(u"FROM student"))
        self.assertTrue(u"student.first_name AS first_name" in sql)
        self.assertTrue(u"student.student_id AS student_id" in sql)
        self.assertTrue(u"student.last_name AS last_name" in sql)
        self.assertTrue(u"student.gpa AS gpa")

    def test_where_expression(self):
        we = UnaryExpression(Student, self.table_expression, WhereExpression(Student, lambda x: x.gpa > 10))
        sql = self.visitor.visit(we)
        self.assertTrue(sql.endswith(u"student.gpa > 10"))

    def test_count_expression(self):
        ce = UnaryExpression(Student, CountExpression(Student), self.table_expression)
        sql = self.visitor.visit(ce)
        self.assertEqual(sql, u"SELECT COUNT(*) FROM student")

    def test_take_expression(self):
        qe = UnaryExpression(Student, SelectExpression(Student, lambda s: s.first_name), self.table_expression)
        te = UnaryExpression(Student, qe, TakeExpression(Student, 1))
        sql = self.visitor.visit(te)
        self.assertEqual(sql, u"SELECT student.first_name AS first_name FROM student LIMIT 1")

    def test_skip_expression(self):
        qe = UnaryExpression(Student, SelectExpression(Student, lambda s: s.first_name), self.table_expression)
        se = UnaryExpression(Student, qe, SkipExpression(Student, 1))
        sql = self.visitor.visit(se)
        self.assertEqual(sql, u"SELECT student.first_name AS first_name FROM student OFFSET 1")

    def test_skip_limit_expression(self):
        qe = UnaryExpression(Student, SelectExpression(Student, lambda s: s.first_name), self.table_expression)
        se = UnaryExpression(Student, qe, SkipExpression(Student, 1))
        te = UnaryExpression(Student, se, TakeExpression(Student, 1))
        sql = self.visitor.visit(te)
        self.assertEqual(sql, u"SELECT student.first_name AS first_name FROM student OFFSET 1 LIMIT 1")

        te = UnaryExpression(Student, qe, TakeExpression(Student, 1))
        se = UnaryExpression(Student, te, SkipExpression(Student, 1))
        sql = self.visitor.visit(se)
        self.assertEqual(sql, u"SELECT student.first_name AS first_name FROM student LIMIT 1 OFFSET 1")
