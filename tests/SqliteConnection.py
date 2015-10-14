__author__ = 'Bruce.Fenske'

import sqlite3
import os
from unittest import TestCase
from tests import _sqlite_db_path
from py_linq.queryable.providers import SqliteDbConnection
from py_linq.queryable.parsers import ProviderConfig
from py_linq.queryable.managers import ConnectionManager
from .TestModels import TestModel, TestModel2, TestPrimary, TestIntUnique, TestForeignKey


class TestSqlite(TestCase):
    def setUp(self):
        self.path = _sqlite_db_path
        self.conn = SqliteDbConnection(self.path)

    def test_connection(self):
        self.assertEqual(self.conn.provider_name, u'sqlite', u'Provider name is wrong')
        self.assertIsInstance(self.conn.provider_config, ProviderConfig, u'Provider config property is not a Provider Config instance')
        self.assertIsNotNone(self.conn.connection, u'Connection is null')
        self.assertIsInstance(self.conn.connection, sqlite3.Connection, u'Connection is not a sqlite3 connection')

    def test_connection_manager(self):
        self.conn = ConnectionManager.get_connection(self.path)
        self.test_connection()

    def test_create_table_int(self):
        sql_testModel = u"CREATE TABLE {0} (int_column INTEGER NULL);".format(TestModel.table_name()).lower()
        sql_testModel2 = u"CREATE TABLE {0} (test_int_column INTEGER NULL);".format(TestModel2.table_name()).lower()

        self.assertEqual(self.conn.create_table(TestModel).lower(), sql_testModel)
        self.assertEqual(self.conn.create_table(TestModel2).lower(), sql_testModel2)

    def test_create_pk(self):
        sql_testModel = u"CREATE TABLE {0} (int_pk INTEGER NOT NULL PRIMARY KEY);".format(TestPrimary.table_name()).lower()
        self.assertEqual(self.conn.create_table(TestPrimary).lower(), sql_testModel)

    def test_create_unique(self):
        sql_testModel = u"CREATE TABLE {0} (int_column INTEGER NULL UNIQUE);".format(TestIntUnique.table_name()).lower()
        self.assertEqual(self.conn.create_table(TestIntUnique).lower(), sql_testModel)

    def test_foreign_key(self):
        sql_testForeignKey = [u"int_pk INTEGER NOT NULL PRIMARY KEY".lower(), u"test_fk INTEGER NOT NULL, FOREIGN KEY(test_fk) REFERENCES test_table(int_pk)".lower()]
        for col_name, col in TestForeignKey.inspect_columns():
            self.assertIn(self.conn._generate_col_sql(col_name, col).lower(), sql_testForeignKey)

    def test_table_creation(self):
        try:
            sql = self.conn.create_table(TestPrimary)
            self.conn.connection.execute(sql)
            sql = self.conn.create_table(TestForeignKey)
            self.conn.connection.execute(sql)
            self.conn.connection.commit()
        except Exception as ex:
            self.conn.connection.rollback()
            raise ex
        finally:
            self.conn.connection.close()

    def tearDown(self):
        if self.conn is not None:
            self.conn.connection.close()
        try:
            os.remove(self.conn.provider_config.db_uri)
        except:
            pass


class TestModelClass(TestCase):

    def test_num_columns(self):
        num_columns = len(TestModel.inspect_columns())
        self.assertEqual(1, num_columns)

    def test_int_column(self):
        self.assertEqual(TestModel.test_int_column.column_name, u'int_column')
        self.assertEqual(TestModel.test_int_column.column_type, int)

        name, col = TestModel2.inspect_columns()[0]
        self.assertEqual(name, u'test_int_column')
        self.assertEqual(TestModel2.test_int_column.column_type, int)

