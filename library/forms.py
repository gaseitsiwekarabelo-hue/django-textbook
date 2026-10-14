from django import forms
from .models import Book


class BookModelForm(forms.ModelForm):
    """
    Form for creating and updating books.
    """

    class Meta:
        model = Book

        fields = [
            "title",
            "author",
            "published_year",
            "genre",
            "is_available",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Enter book title"
            }),
            "author": forms.TextInput(attrs={
                "placeholder": "Enter author name"
            }),
            "published_year": forms.NumberInput(attrs={
                "placeholder": "Enter publication year"
            }),
            "genre": forms.TextInput(attrs={
                "placeholder": "Enter book genre"
            }),
        }

        labels = {
            "title": "Book Title",
            "author": "Author Name",
            "published_year": "Publication Year",
            "genre": "Book Genre",
            "is_available": "Is Available?",
        }

    def clean_title(self):
        title = self.cleaned_data.get("title")

        if title and len(title.strip()) < 3:
            raise forms.ValidationError(
                "The book title must contain at least 3 characters."
            )

        return title


class BookSearchForm(forms.Form):
    """
    Form for searching, filtering, and sorting books.
    """

    q = forms.CharField(
        required=False,
        label="Search Books",
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Search by title, author, or genre..."
        })
    )

    genre = forms.CharField(
        required=False,
        label="Filter by Genre",
        max_length=50,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter a genre"
        })
    )

    sort = forms.ChoiceField(
        required=False,
        label="Sort Books",
        choices=[
            ("title", "Title (A-Z)"),
            ("-title", "Title (Z-A)"),
            ("-published_year", "Newest First"),
            ("published_year", "Oldest First"),
        ],
        initial="title",
    )