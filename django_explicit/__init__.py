from django.db import models


class ResultSet(object):

    def __init__(self, queryset, distinct=False, offset=0, limit=None):
        self.qs = queryset
        if distinct:
            fields = distinct if distinct is not True else []
            self.qs = self.qs.distinct(*fields)
        self.qs = self.qs[offset:limit] if limit else self.qs[offset:]
        try:
            iter(self.qs).next()
        except StopIteration:
            pass

    def __iter__(self):
        return iter(self.qs)

    def __getitem__(self, item):
        return self.qs[item]

    def __len__(self):
        return len(self.qs)

    def __repr__(self):
        return repr(self.qs)

    def values(self):
        return self.qs.values()

    def values_list(self, flat=False):
        return self.qs.values_list(flat=flat)


class QuerySet(object):

    def __init__(self, subject):
        if issubclass(subject, models.Model):
            subject = subject._default_manager
        if isinstance(subject, models.Manager):
            subject = subject.all()
        self.qs = subject

    def __repr__(self):
        return '<QuerySet: %s>' % (self.qs.model.__name__,)

    def annotate(self, **conditions):
        self.qs = self.qs.annotate(**conditions)

    def filter(self, *conditions, **kwconditions):
        self.qs = self.qs.filter(*conditions, **kwconditions)

    def exclude(self, *conditions, **kwconditions):
        self.qs = self.qs.exclude(*conditions, **kwconditions)

    def only(self, *fields):
        self.qs = self.qs.only(*fields)

    def order_by(self, *fields):
        self.qs = self.qs.order_by(*fields)

    def select(self, distinct=False, offset=0, limit=None):
        return ResultSet(
            self.qs, distinct=distinct, offset=offset, limit=limit)

    def select_one(self):
        return self.qs[:2].get()

    def update(self, **fields):
        return self.qs.update(**fields)

    def aggregate(self, **conditions):
        return self.qs.aggregate(**conditions)
