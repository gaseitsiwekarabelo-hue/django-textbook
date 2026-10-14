from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .models import Book
from .forms import BookModelForm, BookSearchForm


def book_list(request):
    """Display, search, filter, sort, and paginate books."""

    search_form = BookSearchForm(request.GET or None)
    books = Book.objects.all()

    query = request.GET.get("q", "").strip()
    genre = request.GET.get("genre", "").strip()
    sort_by = request.GET.get("sort", "title")

    # Search by title, author, or genre.
    if query:
        books = books.filter(
            Q(title__icontains=query)
            | Q(author__icontains=query)
            | Q(genre__icontains=query)
        )

    # Filter by genre.
    if genre:
        books = books.filter(genre__icontains=genre)

    # Sort books using permitted fields.
    sort_options = [
        "title",
        "-title",
        "published_year",
        "-published_year",
    ]

    if sort_by not in sort_options:
        sort_by = "title"

    books = books.order_by(sort_by)

    # Display 5 books per page.
    paginator = Paginator(books, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "books": page_obj,
        "search_form": search_form,
        "query": query,
        "genre": genre,
        "sort_by": sort_by,
    }

    return render(
        request,
        "library/book_list.html",
        context,
    )


def book_detail(request, pk):
    """Display the details of one book."""

    book = get_object_or_404(Book, pk=pk)

    context = {
        "book": book,
    }

    return render(
        request,
        "library/book_detail.html",
        context,
    )


def book_create(request):
    """Create a new book."""

    if request.method == "POST":
        form = BookModelForm(request.POST)

        if form.is_valid():
            book = form.save()

            messages.success(
                request,
                f'"{book.title}" was added successfully.',
            )

            return redirect("book_detail", pk=book.pk)

        messages.error(
            request,
            "Please correct the errors below.",
        )

    else:
        form = BookModelForm()

    context = {
        "form": form,
        "title": "Add a Book",
        "submit_text": "Create Book",
    }

    return render(
        request,
        "library/book_form.html",
        context,
    )


def book_update(request, pk):
    """Update an existing book."""

    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        form = BookModelForm(
            request.POST,
            instance=book,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                f'"{book.title}" was updated successfully.',
            )

            return redirect("book_detail", pk=book.pk)

        messages.error(
            request,
            "Please correct the errors below.",
        )

    else:
        form = BookModelForm(instance=book)

    context = {
        "form": form,
        "book": book,
        "title": f'Edit "{book.title}"',
        "submit_text": "Save Changes",
    }

    return render(
        request,
        "library/book_form.html",
        context,
    )


def book_delete(request, pk):
    """Delete a book after confirmation."""

    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        title = book.title
        book.delete()

        messages.success(
            request,
            f'"{title}" was deleted successfully.',
        )

        return redirect("book_list")

    context = {
        "book": book,
    }

    return render(
        request,
        "library/book_confirm_delete.html",
        context,
    )