from django.test import TestCase
from datetime import date

from .models import Author, Publisher, Genre, Book


class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name='Test',
            last_name='Author'
        )
        self.publisher = Publisher.objects.create(
            name='Test Publisher'
        )
        self.genre = Genre.objects.create(name='Fiction')
        self.book = Book.objects.create(
            title='Test Book',
            isbn='1234567890123',
            publisher=self.publisher,
            genre=self.genre,
            publication_date=date(2020, 1, 1),
            pages=100,
            summary='Test summary',
            rating=5
        )

    def test_string_representation(self):
        self.assertEqual(str(self.book), 'Test Book')

    def test_custom_queryset(self):
        self.assertEqual(Book.objects.high_rated(4).count(), 1)

