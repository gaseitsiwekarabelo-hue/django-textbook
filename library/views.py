from django.shortcuts import render, get_object_or_404, redirect
from .models import Book


def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})


def book_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        published_year = request.POST.get('published_year')
        genre = request.POST.get('genre')
        is_available = request.POST.get('is_available') == 'on'

        Book.objects.create(
            title=title,
            author=author,
            published_year=published_year or None,
            genre=genre,
            is_available=is_available,
        )
        return redirect('book-list')

    return render(request, 'library/book_form.html', {'book': None})


def book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.published_year = request.POST.get('published_year') or None
        book.genre = request.POST.get('genre')
        book.is_available = request.POST.get('is_available') == 'on'
        book.save()

        return redirect('book-list')

    return render(request, 'library/book_form.html', {'book': book})


def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        book.delete()
        return redirect('book-list')

    return render(request, 'library/book_confirm_delete.html', {'book': book})