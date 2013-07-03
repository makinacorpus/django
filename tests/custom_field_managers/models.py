"""
Custom manager for relationship fields.

Using the ``manager`` and ``reverse_manager`` when creating a ForeignKey, you can
choose custom managers used for forward and reverse relationship.
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
