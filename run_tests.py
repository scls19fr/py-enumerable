__author__ = 'Viralogic Software'

import unittest

testclasses = [
    'tests.Constructor',
    'tests.Functions',
    'tests.SqliteConnection',
    'tests.Proxies',
    'tests.ExpressionTreeTest',
    'tests.SqlVisitorTest',
    'tests.QueryableTest'
]
suite = unittest.TestLoader().loadTestsFromNames(testclasses)
unittest.TextTestRunner(verbosity=2).run(suite)
