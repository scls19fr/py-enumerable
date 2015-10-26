__author__ = 'Bruce.Fenske'

from unittest import TestCase
from py_linq.queryable.entity.proxy import DynamicModelProxy
from py_linq.exceptions import InvalidArgumentError
from .TestModels import *


class TestProxy(TestCase):
    def setUp(self):
        self.test_model = TestModel()
        self.test_primary = TestPrimary()
        self.test_foreign_key = TestForeignKey()

    def test_model_instance(self):
        self.assertIsInstance(self.test_model, DynamicModelProxy, u"Test model is not an instance of DynamicModelProxy")
        self.assertIsInstance(self.test_primary, DynamicModelProxy, u"Test primray model is not an instance of DynamicModelProxy")
        self.assertIsInstance(self.test_foreign_key, DynamicModelProxy, u"Test foreign key model is not an instance of DynamicModelProxy")

    def test_set_model_columns(self):
        self.assertIsNone(self.test_model.test_int_column, u"test_int_column should be none")
        self.assertIsNone(self.test_primary.test_pk, u"test_pk column should be none")
        self.assertIsNone(self.test_foreign_key.test_pk, u"test_pk in foreign key model should be none")
        self.assertIsNone(self.test_foreign_key.test_fk, u"test_fk column should be none")

        try:
            self.test_model.test_int_column = 'string'
        except Exception as ex:
            self.assertIsInstance(ex, InvalidArgumentError)

        self.test_model.test_int_column = 1
        self.assertEqual(self.test_model.test_int_column, 1)
        self.assertEqual(self.test_model.columns['test_int_column'].value, 1)
