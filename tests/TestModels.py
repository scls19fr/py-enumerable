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
