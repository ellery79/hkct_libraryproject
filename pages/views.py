from django.shortcuts import render
from books.models import Book
from libraries.models import Library
from libraries.choices import district_choices

# Create your views here.
def index(request):
    books = Book.objects.filter(is_latest =True).order_by('?')[:3]
    context = {
        'books': books,
        'district_choices': district_choices  # Add district_choices to context
    }
    return render(request, 'pages/index.html', context)

def about(request):
    library_query_set = Library.objects.all()
    context = {'library_list': library_query_set}
    return render(request, 'pages/about.html', context)