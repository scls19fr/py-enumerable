import os

from unittest import TestCase

from . import _sqlite_db_path
from py_linq.queryable.expressions.binary import TableExpression
from .TestModels import Student
from py_linq.queryable.db_providers import SqliteDbConnection

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
        self.student2.first_name = u"Dustin"
        self.student2.last_name = u"Mudryk"

        self.conn.add(self.student1)
        self.conn.add(self.student2)
        self.conn.save_changes()

    def test_count(self):
        count = self.conn.query(TableExpression(Student)).count()
        self.assertEquals(count, 2, "Number of students inserted should equal 2 - get {0}".format(count))

    def test_take(self):
        query = self.conn.query(TableExpression(Student)).take(1)
        result = []
        for r in query:
            result.append(r)
        self.assertEquals(len(result), 1, "Appears that take expression is not working")
        self.assertEquals(result[0][0], 1, "Student ID should be 1")

    def tearDown(self):
        if self.conn is not None:
            self.conn.connection.close()
        try:
            os.remove(self.conn.provider_config.db_uri)
        except:
            pass
