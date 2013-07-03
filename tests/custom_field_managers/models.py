"""
23. Giving models a custom manager

You can use a custom ``Manager`` in a particular model by extending the base
``Manager`` class and instantiating your custom ``Manager`` in your model.

There are two reasons you might want to customize a ``Manager``: to add extra
``Manager`` methods, and/or to modify the initial ``QuerySet`` the ``Manager``
returns.
"""

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class ArticlesManager(models.Manager):
    def get_articles_starting_with_a(self):
        return self.filter(name__startswith='a')

class DeletedManager(models.Manager):
    def get_queryset(self):
        return super(DeletedManager, self).get_queryset().filter(deleted=False)


@python_2_unicode_compatible
class Author(models.Model):
    name = models.CharField(max_length=30)
    deleted = models.BooleanField(default=False)


@python_2_unicode_compatible
class Article(models.Model):
    name = models.CharField(max_length=30)
    author = models.ForeignKey(Author, manager=DeletedManager, reverse_manager=ArticlesManager, related_name='articles')

    def __str__(self):
        return self.name
