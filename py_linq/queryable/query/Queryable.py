from ..expressions import *
from ..entity.proxy import DynamicModelProxy
from py_linq import Enumerable
from py_linq.exceptions import NoElementsError


class Queryable(object):
    __class_type__ = None

    def __init__(self, expression, query_provider):
        self.__exp = expression
        self.__provider = query_provider

    def __iter__(self):
        # Get type determined by select expression
        select = self.expression.find(SelectExpression)
        if select is None:
            raise Exception(u"Queryable expression does not contain a SelectExpression")
        num_cols = len(self.type.inspect_columns())
        result_type = None
        if select.func is None:
            result_type = self.type
        else:
            t = LambdaExpression.parse(self.type, select.func)
            print ast.dump(t)
            result_type = t.body.type

        cursor = self.provider.db_provider.connection.cursor()
        cursor.execute(self.sql)
        for r in cursor:
            # if returning just one column
            if len(r) == 1:
                yield r[0]
            # if returning more than one column
            else:
                if result_type == type(list):
                    yield Enumerable(r).select(lambda x: x[0]).to_list()
                elif result_type == type(tuple):
                    yield tuple(Enumerable(r).select(lambda x: x[0]).to_list())
                elif result_type == type(dict):
                    result = {}
                    for i in range(0, len(r), 1):
                        result.__setattr__(cursor.description[i][0], r[i])
                    yield result
                elif result_type == self.type and len(r) == num_cols:
                    proxy = DynamicModelProxy(self.type)
                    for i in range(0, len(r), 1):
                        proxy.__setattr__(cursor.description[i][0], r[i])
                    yield proxy
                else:
                    raise Exception(
                        u"Casting not supported. Please consider using a tuple or dict or list in lambda expression of select"
                    )

    @property
    def provider(self):
        return self.__provider

    @property
    def type(self):
        return self.expression.type

    @property
    def expression(self):
        return self.__exp

    @property
    def sql(self):
        return self.provider.provider_visitor.visit(self.expression)

    def select(self, func):
        self.__exp = UnaryExpression(SelectExpression(self.type, func), self.expression)
        return self

    def count(self):
        self.__exp = CountUnaryExpression(self.type, self.expression)
        return self.provider.db_provider.execute_scalar(self.sql)

    def take(self, limit):
        if isinstance(self.__exp, SkipUnaryExpression):
            self.expression.exp.op.limit = limit
        else:
            self.__exp = TakeUnaryExpression(self.type, self.expression, limit)
        return self

    def skip(self, offset):
        if not isinstance(self.expression, TakeUnaryExpression):
            self.__exp = TakeUnaryExpression(self.type, self.expression, -1)
        self.__exp = SkipUnaryExpression(self.type, self.expression, offset)
        return self

    def first(self):
        raise NotImplementedError()

    def first_or_default(self):
        try:
            return self.first()
        except NoElementsError:
            return None

    def to_list(self):
        return Enumerable(self).to_list()









