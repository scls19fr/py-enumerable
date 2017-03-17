from ..query import IQueryable
from ..providers import IQueryProvider
from ..expressions.unary import LambdaExpression
from ..expressions.expression_tree import ExpressionTree, ModelExpression
from ..expressions.sql import SelectExpression
from ..entity.model import Model


class Queryable(IQueryable):
    def __init__(self, provider, expression_tree=None):
        if not isinstance(provider, IQueryProvider):
            raise TypeError("provider must be an instance of IQueryProvider")
        self._provider = provider

        if not expression_tree is None:
            if not isinstance(expression_tree, ExpressionTree):
                raise TypeError("expression_tree arg must be instance of ExpressionTree")
            self._expression = expression_tree
        else:
            self._expression = ExpressionTree()

    def __iter__(self):
        cursor = self.provider.execute(self.expression)
        row = cursor.fetchone()
        while row is not None:
            #TODO: convert to proxy object required
            yield row
            row = cursor.fetchone()

    @classmethod
    def from_table(cls, provider, table_class):
        if not issubclass(table_class, Model):
            raise TypeError("model must be a subclass of Model")
        cls.__init__(provider, ModelExpression(table_class))

    @property
    def expression(self):
        return self._expression

    @property
    def provider(self):
        return self._provider

    @property
    def sql(self):
        return self.provider.sql

    def select(self, func):
        """
        Used to project model to given properties
        :param func: lambda expression to select properties from model
        :return: IQueryable instance
        """
        select = SelectExpression(self.expression, LambdaExpression(func))
        self.expression.add_node(select)
        return self
