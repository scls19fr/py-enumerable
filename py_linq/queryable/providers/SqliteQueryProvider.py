from ..providers import IQueryProvider
from ..query.queryable import Queryable
from ..visitors.SqliteExpressionVisitor import SqliteExpressionVisitor
from ..db_providers import SqliteDbConnection


class SqliteQueryProvider(IQueryProvider):

    def __init__(self, db_provider):
        self.__visitor = SqliteExpressionVisitor()
        if not isinstance(db_provider, SqliteDbConnection):
            raise TypeError("db_provider arg needs to be a SqliteDbConnection instance")
        self.__provider = db_provider

    @property
    def visitor(self):
        return self.__visitor

    @property
    def db_provider(self):
        return self.__provider

    def createQuery(self, expression):
        return Queryable(self, expression)

    def execute(self, expression):
        expression.visit_children(self.visitor)