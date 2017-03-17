import os
from unittest import TestCase
from . import _sqlite_db_path
from py_linq.queryable.db_providers import SqliteDbConnection
from .TestModels import *


class TestSqliteQuery(TestCase):
    def setUp(self):
        self.path = _sqlite_db_path
        self.conn = SqliteDbConnection(self.path)
        self.query = self.conn.query(TestUpdateModel)

    def test_select_sql(self):
        self.conn.create_table(TestUpdateModel)
        self.conn.save_changes()

        select_text = "SELECT key_column as key, update_column as update_col FROM test_update_table;"
        query = self.query.select(lambda x: (x.key, x.update_col))
        query.provider.execute(query.expression)
        self.assertEqual(query.sql, select_text, "select sql should be {0}: {1}".format(select_text, query.sql))

        self.query = self.conn.query(TestUpdateModel)
        self.query.provider.execute(self.query.expression)
        self.assertEqual(self.query.sql, select_text, "select sql should be {0}: {1}".format(select_text, self.query.sql))


    def tearDown(self):
        if self.conn is not None:
            self.conn.connection.close()
        try:
            os.remove(self.conn.provider_config.db_uri)
        except:
            pass
