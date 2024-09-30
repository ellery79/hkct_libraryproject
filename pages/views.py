from django.shortcuts import render
from books.models import Book
from libraries.models import Library


# Create your views here.
def index(request):
    random3_books_query_set = Book.objects.filter(is_latest=True).order_by('?')[0:3]
    context = {'random3_books_list': random3_books_query_set}

# Create your views here.
#def index(request):
#    random3_books_query_set = Book.objects.filter(is_latest=True).order_by('?')[0:3]
#    context = {'random3_books_list': random3_books_query_set}
def index(request):
    books = Book.objects.filter(is_latest =True)[:3]
    context = {'books': books,
                }
    return render(request, 'pages/index.html', context)

def about(request):
    library_query_set = Library.objects.all()
    context = {'library_list': library_query_set}
    return render(request, 'pages/about.html', context)