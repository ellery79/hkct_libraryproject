from django.shortcuts import render

# Create your views here.
def books(request):
    return render(request, 'books/books.html')

def book(request, book_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    context ={'book': book}
    return render(request, 'books/book.html', context)

def search(request):
    return render(request, 'books/search.html')

