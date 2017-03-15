__author__ = 'Bruce.Fenske'

import sqlite3
import os
import uuid
from unittest import TestCase
from tests import _sqlite_db_path
from py_linq.queryable.db_providers import SqliteDbConnection
from py_linq.queryable.parsers import ProviderConfig
from py_linq.queryable.managers import ConnectionManager
from .TestModels import *


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

    def test_insert_primary(self):
        self._insert_test_primary()

    def test_insert_string_primary(self):
        """
        Note how have to insert primary key manually if the primary key is not int type
        """
        self.conn.create_table(TestPrimaryString)
        self.conn.save_changes()

        pk = unicode(uuid.uuid4())

        primary = TestPrimaryString()
        primary.test_pk = pk
        self.conn.add(primary)
        self.conn.save_changes()

        sql = u"SELECT unicode_pk FROM test_table tt WHERE tt.unicode_pk = '{0}';".format(pk)
        cursor = self.conn.connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], primary.test_pk)
        self.assertEqual(result[0], pk)

    def _insert_test_primary(self):
        self.conn.create_table(TestPrimary)
        self.conn.save_changes()

        test_primary = TestPrimary()
        test_primary.test_pk = self.conn.add(test_primary)
        self.conn.save_changes()

        sql = u"SELECT int_pk FROM test_table tt WHERE tt.int_pk = 1"
        cursor = self.conn.connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], test_primary.test_pk)
        return test_primary

    def test_delete(self):
        test_primary = self._insert_test_primary()
        self.conn.remove(test_primary)
        self.conn.save_changes()

        sql = u"SELECT COUNT(*) FROM test_table tt;"
        cursor = self.conn.connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], 0)

    def test_update(self):
        self.conn.create_table(TestUpdateModel)
        self.conn.save_changes()

        update_test = TestUpdateModel()
        update_test.update_col = 5
        update_test.key = self.conn.add(update_test)
        self.conn.save_changes()

        sql = u"SELECT update_column from test_update_table ut WHERE ut.key_column = {0}".format(update_test.key)
        cursor = self.conn.connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], update_test.update_col)

        update_test.update_col = 10
        self.conn.update(update_test)
        self.conn.save_changes()

        cursor.execute(sql)
        result = cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], update_test.update_col)

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

