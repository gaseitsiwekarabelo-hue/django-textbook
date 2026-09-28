from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q, Count
from django.utils import timezone


# 2.8.1 Abstract base class
class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Author(TimestampedModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    biography = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    class Meta:
        ordering = ['last_name', 'first_name']


class Publisher(TimestampedModel):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    established = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


# Recursive relationship: a genre can have a parent genre.
class Genre(TimestampedModel):
    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subgenres'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


# 2.8.2 Custom QuerySet
class BookQuerySet(models.QuerySet):
    def available(self):
        return self.filter(is_available=True)

    def high_rated(self, threshold=4):
        return self.filter(rating__gte=threshold)

    def recent(self, days=30):
        cutoff = timezone.now().date() - timezone.timedelta(days=days)
        return self.filter(publication_date__gte=cutoff)

    def get_top_rated(self, limit=10):
        return self.order_by('-rating', 'title')[:limit]


class BookManager(models.Manager.from_queryset(BookQuerySet)):
    pass


class Book(TimestampedModel):
    GENRE_CHOICES = [
        ('F', 'Fiction'),
        ('NF', 'Non-Fiction'),
        ('SF', 'Science Fiction'),
        ('FAN', 'Fantasy'),
        ('MYS', 'Mystery'),
        ('THR', 'Thriller'),
        ('ROM', 'Romance'),
        ('HIS', 'Historical'),
        ('BIO', 'Biography'),
        ('SCI', 'Science'),
        ('TEC', 'Technology'),
    ]

    title = models.CharField(max_length=200, help_text="The book's full title")
    subtitle = models.CharField(max_length=200, blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    authors = models.ManyToManyField(
        Author,
        through='BookAuthor',
        related_name='books'
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books'
    )
    publication_date = models.DateField()
    pages = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10000)]
    )
    language = models.CharField(max_length=50, default='English')
    summary = models.TextField()
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    borrowed_count = models.IntegerField(default=0)
    rating = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    objects = BookManager()

    def __str__(self):
        return self.title

    def full_title(self):
        return f"{self.title}: {self.subtitle}" if self.subtitle else self.title

    def can_be_borrowed(self):
        return self.is_available and self.copies.filter(is_borrowed=False).exists()

    def borrow(self, user):
        available_copy = self.copies.filter(is_borrowed=False).first()
        if not available_copy:
            raise ValueError(f"No available copy of {self.title}")

        today = timezone.now().date()
        available_copy.is_borrowed = True
        available_copy.borrowed_by = user
        available_copy.borrowed_date = today
        available_copy.due_date = today + timezone.timedelta(days=14)
        available_copy.save()

        self.borrowed_count += 1
        self.save(update_fields=['borrowed_count', 'updated_at'])
        return available_copy

    @property
    def age(self):
        return (timezone.now().date() - self.publication_date).days // 365

    @classmethod
    def count_by_genre(cls):
        return cls.objects.values('genre').annotate(count=Count('id'))

    def average_rating(self):
        ratings = list(self.reviews.values_list('rating', flat=True))
        return sum(ratings) / len(ratings) if ratings else None

    def clean(self):
        errors = {}
        if self.publication_date and self.publication_date > timezone.now().date():
            errors['publication_date'] = 'Publication date cannot be in the future.'
        if errors:
            raise ValidationError(errors)

    class Meta:
        ordering = ['title']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'publisher'],
                name='unique_book_title_publisher'
            ),
            models.CheckConstraint(
                check=Q(pages__gte=1),
                name='book_pages_positive'
            ),
            models.CheckConstraint(
                check=Q(rating__gte=1) & Q(rating__lte=5),
                name='book_rating_range'
            ),
        ]
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['publication_date']),
            models.Index(fields=['is_available']),
            models.Index(fields=['-publication_date']),
        ]


# Many-to-many through model with extra relationship data.
class BookAuthor(TimestampedModel):
    CONTRIBUTION_CHOICES = [
        ('A', 'Author'),
        ('E', 'Editor'),
        ('C', 'Contributor'),
        ('F', 'Foreword'),
        ('I', 'Introduction'),
        ('T', 'Translator'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    contribution_type = models.CharField(
        max_length=1,
        choices=CONTRIBUTION_CHOICES,
        default='A'
    )
    contribution_order = models.IntegerField(default=1)
    royalty_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.author} - {self.get_contribution_type_display()} of {self.book}"

    class Meta:
        ordering = ['contribution_order']
        constraints = [
            models.UniqueConstraint(
                fields=['book', 'author', 'contribution_type'],
                name='unique_book_author_contribution'
            )
        ]


class BookCopy(TimestampedModel):
    CONDITION_CHOICES = [
        ('E', 'Excellent'),
        ('G', 'Good'),
        ('F', 'Fair'),
        ('P', 'Poor'),
        ('D', 'Damaged'),
    ]

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='copies'
    )
    copy_number = models.PositiveIntegerField()
    condition = models.CharField(
        max_length=1,
        choices=CONDITION_CHOICES,
        default='G'
    )
    location = models.CharField(max_length=100, blank=True)
    is_borrowed = models.BooleanField(default=False)
    borrowed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='borrowed_copies'
    )
    borrowed_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Copy #{self.copy_number} of {self.book.title}"

    class Meta:
        ordering = ['book', 'copy_number']
        constraints = [
            models.UniqueConstraint(
                fields=['book', 'copy_number'],
                name='unique_book_copy_number'
            )
        ]
        indexes = [
            models.Index(fields=['is_borrowed']),
            models.Index(fields=['due_date']),
        ]


class Review(TimestampedModel):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()

    def __str__(self):
        return f"Review of {self.book.title} by {self.user.username}"

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['book', 'user'],
                name='one_review_per_user_per_book'
            )
        ]


# One-to-one relationship.
class UserProfile(TimestampedModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


# Generic relationship: can attach a comment to different models.
class Comment(TimestampedModel):
    content = models.TextField()
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.content[:50]


# 2.8.1 Multi-table inheritance.
class Person(TimestampedModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()


class Librarian(Person):
    employee_number = models.CharField(max_length=30, unique=True)
    department = models.CharField(max_length=100, default='Library')

    def __str__(self):
        return f"{self.full_name()} ({self.employee_number})"


# Proxy model: same database table as Book, different Python behavior/default ordering.
class AvailableBook(Book):
    class Meta:
        proxy = True
        ordering = ['-rating', 'title']

    def days_since_publication(self):
        return (timezone.now().date() - self.publication_date).days


# JSONField example.
class UserPreferences(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferences = models.JSONField(default=dict)

    def __str__(self):
        return f"Preferences for {self.user.username}"

# Create your models here.
