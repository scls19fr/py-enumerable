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

    @property
    def sql(self):
        return "{0}{1}".format(self.__selects, self.__from)

    def createQuery(self, expression):
        return Queryable(self, expression)

    def execute(self, expression):
        expression.visit_children(self.visitor)
        expression.visit(self.visitor)
        cursor = self.db_provider.connection.cursor()
        cursor.execute(self.sql)

    @property
    def __selects(self):
        if not self.visitor.sql_expression_result.has_projections:
            return "SELECT * "
        selects = ", ".join(self.visitor.sql_expression_tree['select'])
        return "SELECT {0} ".format(selects)

    @property
    def __from(self):
        if not self.visitor.sql_expression_result.has_source_name:
            raise Exception("no source or table name found for expression")
        return "FROM {0}".format(self.visitor.sql_expression_result.source)
