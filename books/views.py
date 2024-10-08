from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Library
from books.choices import status_choices
from libraries.choices import district_choices
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

# Create your views here.
def books(request):
    books = Book.objects.all()
    paginator = Paginator(books, 6)
    #GET is htmlResponse method while get is a function.
    page = request.GET.get('page')
    paged_books = paginator.get_page(page)
    # pass database records into books context. Make a dictionary
    context = {'books': paged_books}
    return render(request, 'books/books.html', context) 

def book(request, book_id):
    # Retrieve the book by its ID
    book = get_object_or_404(Book, pk=book_id) 
    # Filter books with the specified title and "Available" status
    available_books = Book.objects.filter(title=book.title, book_status="Available")
    # Get unique districts from the related Library
    districts = available_books.values_list('library__district', flat=True).distinct()
    context = {
        'book': book,
        'districts': districts,
        'user': request.user,
    }
    if request.method == 'POST':
        if request.user.is_authenticated:
            messages.success(request, 'You have already reserved this book.')
            return redirect('/books/'+book_id)  

    #reserve_limit = user.rule.reserve_limit
    #new_reserve = Reserve(reserve_date = datetime.now(),reserve_status = 'active', book=selected_book, user=user)
    #if len(new_reserve) < reserve_limit:
    #    new_reserve.save()
    return render(request, 'books/book.html', context)

def search(request):
    queryset_list = Book.objects.all()
    print("District Choices:", district_choices)  # Debugging output
    print("Request GET:", request.GET)  # Check what values are being sent
    # Rest of your filtering logic...
    if 'keywords' in request.GET: # check if existence of key words in search
        keywords = request.GET['keywords'] #if words entered, put such words into "keywords"
        if keywords:
            queryset_list = queryset_list.filter(
                description__icontains=keywords #icontains means case insensitive
            )
    if 'title' in request.GET: # check if existence of key words in search
        title = request.GET['title'] #if words entered, put such words into
        if title:
            queryset_list = queryset_list.filter(
                title__icontains=title #words contained are fine
            )
    if 'library' in request.GET:
        library = request.GET['library']
        if library:
            queryset_list = queryset_list.filter(
                library__district__iexact=library  # Assuming 'district' is the field in Library
            )
    if 'author' in request.GET: # check if existence of key words in search
        author = request.GET['author'] #if words entered, put such words into
        if author:
            queryset_list = queryset_list.filter(
                author__icontains=author #words contained are fine
            )
    if 'publisher' in request.GET: # check if existence of key words in search
        publisher = request.GET['publisher'] #if words entered, put such words into
        if publisher:
            queryset_list = queryset_list.filter(
                publisher__icontains=publisher #words contained are fine
            )
    context = {
        'district_choices': district_choices,
        'status_choices': status_choices,
        'books': queryset_list,
        'values': request.GET
    }
    return render(request, 'books/search.html', context)
