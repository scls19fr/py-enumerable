__author__ = 'Viralogic Software'

import unittest

testclasses = [
    'tests.Constructor',
    'tests.Functions',
    'tests.SqliteConnection',
    'tests.Proxies',
    'tests.Expressions'
]
suite = unittest.TestLoader().loadTestsFromNames(testclasses)
unittest.TextTestRunner(verbosity=2).run(suite)
