import abc


class IExpressionVisitor(object):
    @abc.abstractmethod
    def visit(self, expression):
        raise NotImplementedError()


class SqlVisitorResultModel(object):
    projection = None
    source = None
    filters = []

    @property
    def has_projections(self):
        return self.projection is not None and len(self.projection) > 0

    @property
    def has_source_name(self):
        return self.source is not None and len(self.source) > 0



