# library/admin.py
from django.contrib import admin
from .models import Author, Book, Publisher

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'birth_date')
    search_fields = ('last_name', 'first_name')

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'publication_date', 'is_available', 'rating')
    list_filter = ('genre', 'is_available', 'publication_date')
    search_fields = ('title', 'isbn', 'author__last_name')