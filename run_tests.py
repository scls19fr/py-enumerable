import unittest

testclasses = [
    'tests.Constructor',
    'tests.Functions',
    'tests.SqliteConnection',
    'tests.Proxies',
    'tests.ExpressionTreeTest',
    'tests.QueryableTest',
    'tests.LambdaExpression'
]
suite = unittest.TestLoader().loadTestsFromNames(testclasses)
unittest.TextTestRunner(verbosity=2).run(suite)
