__author__ = 'Bruce.Fenske'

import sqlite3
import os
from unittest import TestCase
from tests import _sqlite_db_path
from py_linq.queryable.providers import SqliteDbConnection
from py_linq.queryable.parsers import ProviderConfig


class TestSqlite(TestCase):
    def setUp(self):
        self.path = _sqlite_db_path
        self.conn = SqliteDbConnection(self.path)

    def test_connection(self):
        self.assertIsInstance(self.conn.provider_config, ProviderConfig, 'Provider config property is not a Provider Config instance')
        self.assertEqual(self.conn.provider_config.provider_name, 'sqlite', 'Provider name property is not sqlite')
        self.assertIsNotNone(self.conn.connection, 'Connection is null')
        self.assertIsInstance(self.conn.connection, sqlite3.Connection, 'Connection is not a sqlite3 connection')

    def tearDown(self):
        if self.conn is not None:
            self.conn.connection.close()
        try:
            os.remove(self.conn.provider_config.db_uri)
        except:
            pass
