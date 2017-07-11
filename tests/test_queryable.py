import os

from unittest import TestCase

from . import _sqlite_db_path
from py_linq.queryable.expressions.binary import TableExpression
from .models import Student
from py_linq.queryable.db_providers import SqliteDbConnection
from py_linq.exceptions import NoElementsError


class QueryableTest(TestCase):
    def setUp(self):
        self.path = _sqlite_db_path
        self.conn = SqliteDbConnection(self.path)

        self.conn.create_table(Student)
        self.conn.save_changes()

        self.student1 = Student()
        self.student1.student_id = 1
        self.student1.first_name = u"Bruce"
        self.student1.last_name = u"Fenske"

        self.student2 = Student()
        self.student2.student_id = 2
        self.student2.first_name = u"Abraham"
        self.student2.last_name = u"Mudryk"

        self.conn.add(self.student1)
        self.conn.add(self.student2)
        self.conn.save_changes()

    def test_count(self):
        count = self.conn.query(TableExpression(Student)).count()
        self.assertEquals(count, 2, "Number of students inserted should equal 2 - get {0}".format(count))

    def test_take(self):
        result = self.conn.query(TableExpression(Student)).take(1).to_list()
        self.assertEquals(len(result), 1, u"Appears that take expression is not working")
        self.assertEquals(result[0].student_id, 1, u"Student ID should be 1 - get {0}".format(result[0].student_id))
        self.assertEquals(result[0].first_name, u"Bruce", u"Bruce should be the first name - get {0}".format(result[0].first_name))
        self.assertEquals(result[0].last_name, u"Fenske", u"Fenske should be the last name - get {0}".format(result[0].last_name))

        result = self.conn.query(TableExpression(Student)).skip(1).take(1).to_list()
        self.assertEquals(len(result), 1, u"Appears that skip then take is not working")
        self.assertEquals(result[0].student_id, 2, u"Student ID should be 2 - get {0}".format(result[0].student_id))
        self.assertEquals(result[0].first_name, u"Abraham", u"Abraham should be the first name - get {0}".format(result[0].first_name))
        self.assertEquals(result[0].last_name, u"Mudryk",u"Mudryk should be the last name - get {0}".format(result[0].last_name))

    def test_skip(self):
        result = self.conn.query(TableExpression(Student)).skip(1).to_list()
        self.assertEquals(len(result), 1, u"Appears that take expression is not working")
        self.assertEquals(result[0].student_id, 2, u"Student ID should be 2 - get {0}".format(result[0].student_id))
        self.assertEquals(result[0].first_name, u"Abraham", u"Abraham should be the first name - get {0}".format(result[0].first_name))
        self.assertEquals(result[0].last_name, u"Mudryk", u"Mudryk should be the last name - get {0}".format(result[0].last_name))

        result = self.conn.query(TableExpression(Student)).take(1).skip(1).to_list()
        self.assertEquals(len(result), 1, u"Appears that take expression is not working")
        self.assertEquals(result[0].student_id, 2, u"Student ID should be 2 - get {0}".format(result[0].student_id))
        self.assertEquals(result[0].first_name, u"Abraham", u"Abraham should be the first name - get {0}".format(result[0].first_name))
        self.assertEquals(result[0].last_name, u"Mudryk", u"Mudryk should be the last name - get {0}".format(result[0].last_name))

    def test_first(self):
        result = self.conn.query(TableExpression(Student)).first()
        self.assertEquals(result.student_id, 1, u"Student ID should be 1 - get {0}".format(result.student_id))
        self.assertEquals(result.first_name, u"Bruce", u"Bruce should be the first name - get {0}".format(result.first_name))
        self.assertEquals(result.last_name, u"Fenske", u"Fenske should be the last name - get {0}".format(result.last_name))

        self.conn.remove(self.student1)
        self.conn.remove(self.student2)
        self.conn.save_changes()

        self.assertRaises(NoElementsError, self.conn.query(TableExpression(Student)).first)

    def test_first_or_default(self):
        self.conn.remove(self.student1)
        self.conn.save_changes()

        result = self.conn.query(TableExpression(Student)).first_or_default()
        self.assertEquals(result.student_id, 2, u"Student ID should be 2 - get {0}".format(result.student_id))
        self.assertEquals(result.first_name, u"Abraham", u"Abraham should be the first name - get {0}".format(result.first_name))
        self.assertEquals(result.last_name, u"Mudryk", u"Mudryk should be the last name - get {0}".format(result.last_name))

        self.conn.remove(self.student2)
        self.conn.save_changes()
        result = self.conn.query(TableExpression(Student)).first_or_default()
        self.assertIsNone(result, "First or Default query should be none. The Student table is empty")


    def tearDown(self):
        if self.conn is not None:
            self.conn.connection.close()
        try:
            os.remove(self.conn.provider_config.db_uri)
        except:
            pass
