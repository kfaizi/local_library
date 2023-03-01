from django.shortcuts import render
from .models import Book, Author, BookInstance, Language
from django.views import generic

def index(request):
    """View func for site homepage."""

    # count the main objects
    num_books = Book.objects.all().count()
    num_copies = BookInstance.objects.all().count()
    num_authors = Author.objects.all().count()

    # available books
    num_copies_available = BookInstance.objects.filter(status__exact='a').count()

    context = {
        'num_books': num_books,
        'num_copies': num_copies,
        'num_authors': num_authors,
        'num_copies_available': num_copies_available,
    }

    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    # context_object_name = 'book_list'  # custom name for list as template var
