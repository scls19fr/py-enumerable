__author__ = 'Bruce.Fenske'

from py_linq.queryable.entity.model import Model
from py_linq.queryable.entity.column_types import Column, PrimaryKey, ForeignKey

class TestModel(Model):
    __table_name__ = u'test_table'
    test_int_column = Column(int, 'int_column')


class TestModel2(Model):
    __table_name__ = u'test_table'
    test_int_column = Column(int)


class TestPrimary(Model):
    __table_name__ = u"test_table"
    test_pk = PrimaryKey(int, 'int_pk')


class TestPrimaryString(Model):
    __table_name__ = u"test_table"
    test_pk = PrimaryKey(unicode, 'unicode_pk')


class TestIntUnique(Model):
    __table_name__ = u"test_table"
    test_pk = PrimaryKey(int)
    test_unique = Column(int, 'int_column', is_unique=True)

class TestForeignKey(Model):
    __table_name__ = u"foreign_key_table"
    test_pk = PrimaryKey(int, 'int_pk')
    test_fk = ForeignKey(TestPrimary, 'test_fk', is_nullable=False)

class TestUpdateModel(Model):
    __table_name__ = u"test_update_table"
    key = PrimaryKey(int, 'key_column')
    update_col = Column(int, 'update_column')

class Student(Model):
    __table_name__ = u"student"
    student_id = PrimaryKey(int, "student_id")
    first_name = Column(unicode, "first_name")
    last_name = Column(unicode, "last_name")

