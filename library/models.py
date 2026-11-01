# library/models.py
from django.conf import settings
from django.db import models
from django.urls import reverse


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    GENRE_CHOICES = [
        ('fiction', 'Fiction'),
        ('non_fiction', 'Non-Fiction'),
        ('sci_fi', 'Science Fiction'),
        ('fantasy', 'Fantasy'),
        ('mystery', 'Mystery'),
        ('biography', 'Biography'),
        ('history', 'History'),
        ('tech', 'Technology'),
    ]

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    isbn = models.CharField('ISBN', max_length=13, unique=True, blank=True, null=True)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='fiction')
    pages = models.PositiveIntegerField(null=True, blank=True)
    summary = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    language = models.CharField(max_length=50, default='English')
    is_available = models.BooleanField(default=True)
    rating = models.PositiveIntegerField(null=True, blank=True)
    
    # Tracks who created the book (utilized in view permission checks)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='books_created'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('library:book-detail', kwargs={'pk': self.pk})