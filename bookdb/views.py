from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Book, Author, Genre, Library, Availability
from .forms import BookForm
from django.db.models import Q


def home(request):
    return render(request, 'home.html')


def book_list(request):
    books = Book.objects.select_related('author', 'genre', 'availability')
    return render(request, 'book_list.html', {'books': books})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # Inline recommendations for the detail page (show a few similar books)
    genre_recs = Book.objects.filter(genre=book.genre).exclude(pk=book.pk).select_related('author', 'genre', 'availability')[:4]
    return render(request, 'book_detail.html', {'book': book, 'genre_recs': genre_recs})


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            # Get or create related objects from provided names
            author_name = form.cleaned_data.pop('author_name')
            # genre is now a ModelChoiceField and returns a Genre instance
            genre = form.cleaned_data.pop('genre')
            library_name = form.cleaned_data.pop('library_name')
            availability_status = form.cleaned_data.pop('availability_status')

            author, _ = Author.objects.get_or_create(name=author_name)
            library, _ = Library.objects.get_or_create(name=library_name, defaults={'area': '', 'total_books': 0})
            availability, _ = Availability.objects.get_or_create(status=availability_status)

            book = form.save(commit=False)
            book.author = author
            book.genre = genre
            book.library = library
            book.availability = availability
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})


def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            author_name = form.cleaned_data.pop('author_name')
            genre = form.cleaned_data.pop('genre')
            library_name = form.cleaned_data.pop('library_name')
            availability_status = form.cleaned_data.pop('availability_status')

            author, _ = Author.objects.get_or_create(name=author_name)
            library, _ = Library.objects.get_or_create(name=library_name, defaults={'area': '', 'total_books': 0})
            availability, _ = Availability.objects.get_or_create(status=availability_status)

            book = form.save(commit=False)
            book.author = author
            book.genre = genre
            book.library = library
            book.availability = availability
            book.save()
            return redirect('book_detail', pk=book.pk)
    else:
        related_initial = {
            'author': book.author.name if book.author else '',
            'genre': book.genre.pk if book.genre else None,
            'library': book.library.name if book.library else '',
            'availability': book.availability.status if book.availability else '',
        }
        form = BookForm(instance=book, related_initial=related_initial)
    return render(request, 'edit_book.html', {'form': form, 'book': book})


def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'delete_book.html', {'book': book})


def search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__name__icontains=query) |
            Q(genre__name__icontains=query)
        ).select_related('author', 'genre', 'availability', 'library')
    return render(request, 'search.html', {'results': results, 'query': query})


def recommendations(request, pk=None):
    """
    Provide richer recommendations:
    - by_genre: books sharing the same genre (ordered by published_year desc)
    - by_author: books by the same author
    - recent: recently published books across the library
    If `pk` provided, the current book will be excluded from results.
    """
    # Recommendations based only on genre.
    current = None
    qs = Book.objects.select_related('author', 'genre', 'availability')

    if pk is not None:
        current = get_object_or_404(Book, pk=pk)
        # books in same genre, exclude current
        recommended = qs.filter(genre=current.genre).exclude(pk=current.pk).order_by('-published_year')[:12]
        return render(request, 'recommendations.html', {
            'current': current,
            'recommended': recommended,
        })
    else:
        # Site-wide: show top recent books grouped by genre
        genres = Genre.objects.all()
        grouped = []
        for g in genres:
            books = qs.filter(genre=g).order_by('-published_year')[:6]
            if books.exists():
                grouped.append((g, books))
        return render(request, 'recommendations.html', {
            'current': None,
            'grouped': grouped,
        })


def api_books(request):
    books = Book.objects.select_related('author', 'genre', 'library', 'availability').all()
    data = []
    for b in books:
        data.append({
            'id': b.pk,
            'title': b.title,
            'author': b.author.name,
            'genre': b.genre.name,
            'library': b.library.name,
            'availability': b.availability.status,
        })
    return JsonResponse(data, safe=False)


def api_book_detail(request, pk):
    b = get_object_or_404(Book.objects.select_related('author', 'genre', 'library', 'availability'), pk=pk)
    data = {
        'id': b.pk,
        'title': b.title,
        'author': b.author.name,
        'genre': b.genre.name,
        'library': b.library.name,
        'availability': b.availability.status,
    }
    return JsonResponse(data)


def api_index(request):
    """Render a simple API documentation page describing available endpoints."""
    sample = {
        "id": 1,
        "title": "Book Title",
        "author": "Author Name",
        "genre": "History",
        "library": "Mysuru Public Library",
        "availability": "Yes"
    }
    endpoints = [
        {'path': '/api/books/', 'method': 'GET', 'desc': 'List all books'},
        {'path': '/api/books/<id>/', 'method': 'GET', 'desc': 'Get details for a single book by id'},
    ]
    return render(request, 'api.html', {'endpoints': endpoints, 'sample': sample})
