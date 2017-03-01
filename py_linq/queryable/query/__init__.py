import abc
from ..interfaces import IQueryable, IQueryProvider


class Queryable(IQueryable):
    _provider = None
    _expression = None

    def __init__(self, provider, expression = None):
        """
        Construct a Queryable instance from a provider
        :param provider: IQueryableProvider instance
        :param expression: Expression instance
        """
        if provider is None:
            raise TypeError("provider argument cannot be None")
        if not issubclass(provider, IQueryProvider):
            raise TypeError("provider must implement IQueryProvider")
        if expression is None:
            raise NotImplementedError()
        # TODO: Need to extend constructor to handle expression argument once expression is built
        self._provider = provider
        self._expression = expression

    @property
    def provider(self):
        return self._provider

    @property
    def expression(self):
        return self._expression

    def __iter__(self):
        return self.provider.execute(self.expression)


class QueryProviderAbstractBase(IQueryProvider):

    def __init__(self):
        """
        Default constructor. Does nothing
        :return: None
        """
        pass

    def createQuery(self, expression):
        return Queryable(self, expression)

    @abc.abstractmethod
    def execute(self, expression):
        raise NotImplementedError()