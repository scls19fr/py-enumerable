__author__ = 'Bruce.Fenske'

import sqlite3
import os
from unittest import TestCase
from tests import _sqlite_db_path
from py_linq.queryable.providers import SqliteDbConnection
from py_linq.queryable.parsers import ProviderConfig
from py_linq.queryable.managers import ConnectionManager
from py_linq.queryable.entity.proxy import DynamicModelProxy
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

    def test_table_creation(self):
        self.conn.create_table(TestPrimary)
        self.conn.create_table(TestForeignKey)
        self.conn.save_changes()

        sql = u"SELECT name FROM sqlite_master WHERE type='table' AND name='{0}';"
        sql_primary = sql.format(TestPrimary.table_name())
        cursor = self.conn.connection.cursor()
        cursor.execute(sql_primary)
        result = cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[0].lower(), TestPrimary.table_name().lower())

        sql_foreign = sql.format(TestForeignKey.table_name())
        cursor = self.conn.connection.cursor()
        cursor.execute(sql_foreign)
        result = cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[0].lower(), TestForeignKey.table_name().lower())

    def test_index_creation(self):
        self.conn.create_table(TestIntUnique)
        self.conn.create_indexes(TestIntUnique)
        self.conn.save_changes()

        sql = u"SELECT name FROM sqlite_master WHERE type = 'index' AND name='{0}';"
        unique_column = filter(lambda c: c[1].is_unique, TestIntUnique.inspect_columns())
        if len(unique_column) != 1:
            raise Exception(u"Incorrect number of unique columns in {0}".format(TestIntUnique.table_name()))
        column_name = unique_column[0][0]
        index_name = u"{0}_index".format(column_name)
        unique_sql = sql.format(index_name)
        cursor = self.conn.connection.cursor()
        cursor.execute(unique_sql)
        result = cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[0].lower(), index_name.lower())

    def test_insert(self):
        self.conn.create_table(TestPrimary)
        self.conn.save_changes()

        test_primary = TestPrimary()
        test_primary_proxy = DynamicModelProxy.create_proxy_from_model_instance(test_primary)
        test_primary.test_pk = self.conn.add(test_primary_proxy)
        self.conn.save_changes()

        sql = u"SELECT int_pk FROM test_table tt WHERE tt.int_pk = 1"
        cursor = self.conn.connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], test_primary.test_pk)


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

