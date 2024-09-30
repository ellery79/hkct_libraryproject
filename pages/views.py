from django.shortcuts import render
from books.models import Book

# Create your views here.
def index(request):
    books = Book.objects.filter(is_latest =True)[:3]
    context = {'books': books,
                }
    return render(request, 'pages/index.html', context)

def about(request):
    return render(request, 'pages/about.html')