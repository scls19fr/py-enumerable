__author__ = 'Bruce.Fenske'

import sqlite3
import os
from unittest import TestCase
from tests import _sqlite_db_path, TestModel, TestModel2
from py_linq.queryable.providers import SqliteDbConnection
from py_linq.queryable.parsers import ProviderConfig
from py_linq.queryable.managers import ConnectionManager
from py_linq.queryable.entity.model import Column


class TestSqlite(TestCase):
    def setUp(self):
        self.path = _sqlite_db_path
        self.conn = SqliteDbConnection(self.path)

    def test_connection(self):
        self.assertEqual(self.conn.provider_name, 'sqlite', 'Provider name is wrong')
        self.assertIsInstance(self.conn.provider_config, ProviderConfig, 'Provider config property is not a Provider Config instance')
        self.assertIsNotNone(self.conn.connection, 'Connection is null')
        self.assertIsInstance(self.conn.connection, sqlite3.Connection, 'Connection is not a sqlite3 connection')

    def test_connection_manager(self):
        self.conn = ConnectionManager.get_connection(self.path)
        self.test_connection()

    def tearDown(self):
        if self.conn is not None:
            self.conn.connection.close()
        try:
            os.remove(self.conn.provider_config.db_uri)
        except:
            pass


class TestModelClass(TestCase):
    def setUp(self):
        self.test_table = TestModel()
        self.test_table2 = TestModel2()

    def test_num_columns(self):
        num_columns = len(self.test_table.inspect_columns())
        self.assertEqual(1, num_columns)

    def test_int_column(self):
        self.assertEqual(self.test_table.test_int_column.column_name, 'int_column')
        self.assertEqual(self.test_table.test_int_column.column_type, type(int))

        name, col = self.test_table2.inspect_columns()[0]
        self.assertEqual(name, 'test_int_column')
        self.assertEqual(self.test_table2.test_int_column.column_type, type(int))