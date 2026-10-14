from django.urls import path
from . import views


app_name = "library"


urlpatterns = [
    # Display all books.
    path("", views.book_list, name="book_list"),

    # Add a new book.
    path("add/", views.book_create, name="book_create"),

    # Display one book.
    path("<int:pk>/", views.book_detail, name="book_detail"),

    # Update an existing book.
    path("<int:pk>/edit/", views.book_update, name="book_update"),

    # Delete a book.
    path("<int:pk>/delete/", views.book_delete, name="book_delete"),
]