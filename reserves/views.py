from django.shortcuts import render

# Create your views here.

def reserve(request):
    return render(request, 'books/book.html')