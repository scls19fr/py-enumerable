__author__ = 'Bruce.Fenske'

from unittest import TestCase
from py_linq.queryable.entity.proxy import DynamicModelProxy
from py_linq.exceptions import InvalidArgumentError
from .TestModels import *


class TestProxy(TestCase):
    def setUp(self):
        self.test_model = TestModel()
        self.test_primary = TestPrimary()
        self.test_primary_string = TestPrimaryString()

    def test_primary_key(self):
        self.assertEqual(self.test_primary.test_pk, 0)
        self.assertEqual(self.test_primary_string.test_pk, '')

    def test_set_columns(self):
        self.test_model.test_int_column = 5
        proxy = DynamicModelProxy.create_proxy_from_model_instance(self.test_model)
        self.assertEqual(proxy.test_int_column, self.test_model.test_int_column)

        self.test_model = TestModel()
        self.test_model.test_int_column = "string"
        self.assertRaises(InvalidArgumentError, DynamicModelProxy.create_proxy_from_model_instance, self.test_model)

        test_model1 = TestModel()
        test_model1.test_int_column = 5
        test_model2 = TestModel()
        test_model2.test_int_column = 10
        proxy1 = DynamicModelProxy.create_proxy_from_model_instance(test_model1)
        proxy2 = DynamicModelProxy.create_proxy_from_model_instance(test_model2)
        self.assertNotEqual(proxy1.test_int_column, proxy2.test_int_column)


