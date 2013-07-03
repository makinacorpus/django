from __future__ import absolute_import

from django.test import TestCase
from django.utils import six

from .models import Author, Article, ArticlesManager


class CustomFieldsManagerTests(TestCase):
    def test_manager(self):
        author = Author.objects.create(name='The author')
        article = Article.objects.create(name='The article', author=author)

        # Let's see if we have our custom ArticlesManager, for the reverse relationship.
        self.assertIsInstance(author.articles, ArticlesManager)
        self.assertQuerysetEqual(author.articles.get_articles_starting_with_a(), [])

        self.assertEqual(article.author, author)

        author.deleted = True
        author.save()

        article = Article.objects.all()[0] # If we reuse the same article, the author is cached.

        # Because our forward manager will mask a deleted author, this will raise an exception.
        self.assertRaises(Author.DoesNotExist, lambda: article.author)
