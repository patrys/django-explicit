django-explicit
===============

This is an experiment to explore the possibility of having an ORM that does not allow you to accidentally shoot yourself in the foot.

```python
from myapp import models
from django_explicit import QuerySet

qs = QuerySet(models.Movie)
qs.filter(released__year=1982)
qs.order_by('title')
print repr(qs)
# <QuerySet: Movie>
rs = qs.select(limit=10)  # Execute the query
print type(rs)
# <class 'django_explicit.ResultSet'>
print rs
# [Movie(id=42)]
```

`django_explicit.QuerySet` is not iterable and will not evaluate the queryset until explicitly told to do so.

`django_explicit.ResultSet` will evaluate a queryset exactly once.
