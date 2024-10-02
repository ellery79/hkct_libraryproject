from django.shortcuts import render, get_object_or_404
from .models import Book
# Create your views here.

def books(request):
    return render(request, 'books/books.html')

def book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    context ={'book': book}
    return render(request, 'books/book.html', context)

def search(request):
    return render(request, 'books/search.html')

