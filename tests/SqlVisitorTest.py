from unittest import TestCase

from py_linq.queryable.db_providers import SqliteDbConnection
from py_linq.queryable.expressions import CountExpression
from py_linq.queryable.expressions.binary import *
from py_linq.queryable.providers.SqliteQueryProvider import SqliteQueryProvider
from py_linq.queryable.query.Queryable import Queryable
from py_linq.queryable.visitors.sql import SqlVisitor
from . import _sqlite_db_path
from .TestModels import Student


class SqlVisitorTest(TestCase):
    def setUp(self):
        #self.student1 = Student()
        #self.student.student_id = 1
        #self.student.first_name = "Bruce"
        #self.student.last_name = "Fenske"

        #self.student2 = Student()
        #self.student.student_id = 2
        #self.student.first_name = "Dustin"
        #self.student.last_name = "Mudryk"

        self.select_text = "SELECT student_id AS student_id, first_name AS first_name, last_name AS last_name"
        self.table_select_sql = self.select_text + " FROM " + Student.__table_name__
        self.table_expression = TableExpression(Student)
        self.visitor = SqlVisitor()

    def test_left(self):

        self.assertIsInstance(self.table_expression.left, SelectExpression)
        visitor_sql = self.visitor.visit(self.table_expression.left).value
        self.assertEquals(visitor_sql.lower(), self.select_text.lower(), "{0} does not match {1} - SelectExpression".format(
            visitor_sql,
            self.select_text
        ))

    def test_operator(self):
        self.assertIsInstance(self.table_expression.operator, StringExpression)
        desired_text = "FROM"
        visitor_sql = self.visitor.visit(self.table_expression.operator).value
        self.assertEquals(visitor_sql.lower(), desired_text.lower(), "{0} does not match {1} - StringExpression table operator".format(
            visitor_sql,
            desired_text
        ))

    def test_right(self):
        self.assertIsInstance(self.table_expression.right, StringExpression)
        visitor_sql = self.visitor.visit(self.table_expression.right).value
        self.assertEquals(visitor_sql.lower(), Student.__table_name__.lower(), "{0} does not match {1} - StringExpression".format(
            visitor_sql,
            Student.__table_name__
        ))

    def test_table_expression(self):
        visitor_sql = self.visitor.visit(self.table_expression).value
        self.assertEquals(visitor_sql.lower(), self.table_select_sql.lower(), "{0} does not match {1} - TableExpression".format(
            visitor_sql,
            self.table_select_sql
        ))

    def test_count_expression(self):
        count_expression = BinaryExpression(Student, CountExpression(Student), StringExpression(Student, "FROM"), StringExpression(Student, Student.__table_name__))
        visitor_sql = self.visitor.visit(count_expression).value
        desired_sql = "SELECT COUNT(*) FROM student"
        self.assertEquals(visitor_sql.lower(), desired_sql.lower(), "{0} does not match {1} - CountExpression".format(
            visitor_sql,
            desired_sql
        ))

    def test_queryable_generation(self):
        db_provider = SqliteDbConnection(_sqlite_db_path)
        provider = SqliteQueryProvider(db_provider)
        queryable = provider.createQuery(self.table_expression)
        self.assertIsInstance(queryable, Queryable)

        self.assertEquals(queryable.sql.lower(), self.table_select_sql.lower(), "{0} does not match {1} - SqliteQueryProvider".format(
            queryable.sql,
            self.table_select_sql
        ))

    def tearDown(self):
        self.table_expression = None
        self.visitor = None
        #self.student1 = self.student2 = None



