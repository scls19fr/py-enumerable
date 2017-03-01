import abc

class IQueryable(object):
    '''
    Interface to implement IQueryable. Container to hold expression and provider
    '''
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def expression(self):
        '''
        Expression tree associated with the instance of IQueryable
        :return: Expression tree associated with IQueryable instance
        '''
        return NotImplementedError()

    @abc.abstractproperty
    def provider(self):
        '''
        Query provider associated with the data source/data base
        :return: IQueryProvider instance
        '''
        return NotImplementedError()

class IQueryProvider(object):
    '''
    Interface to implement IQueryProvider. Also necessary for builing query expression
    '''
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def createQuery(self, expression):
        '''
        Creates SQL query from expression tree
        :param expression: an expression tree instance
        :return: IQueryable instance
        '''
        return NotImplementedError()

    @abc.abstractmethod
    def execute(self, expression):
        '''
        Creates an iterable to enumerable over from given expression.
        :param expression: An expression tree instance
        :return: iterable object --> database cursor
        '''
        return NotImplementedError()

