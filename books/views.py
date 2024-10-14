"""
Views module for the Books application.

This module contains view functions to handle book listings, detailed
book views, and search functionalities within the library system.
"""

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils import timezone

from books.models import status_choices
from libraries.models import district_choices
from reserves.models import Reserve
from accounts.views import update_book_reserve_status
from .models import Book

# Create your views here.


def books(request):
    """
    Display a paginated list of all available books.

    Retrieves all book records from the database, paginates them,
    and renders the 'books.html' template with the paginated books.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML page displaying the books.
    """
    books = Book.objects.all()
    paginator = Paginator(books, 6)
    # Retrieve the current page number from the GET parameters
    page = request.GET.get('page')
    paged_books = paginator.get_page(page)
    # pass database records into books context. Make a dictionary
    context = {'books': paged_books}
    return render(request, 'books/books.html', context)


def book(request, book_id):
    """
    Display detailed information about a specific book and handle reservations.

    Fetches the selected book by its ID and retrieves other available copies
    with the same ISBN. If the user is authenticated, it also fetches their
    active reservations. Handles POST requests to reserve a book, enforcing
    reserve limits based on user rules.

    Args:
        request (HttpRequest): The HTTP request object.
        book_id (int): The ID of the book to display.

    Returns:
        HttpResponse: Rendered HTML page with book details or a redirect after reservation.
    """
    update_book_reserve_status()
    selected_book = Book.objects.get(id=book_id)
    books = Book.objects.filter(
        isbn=selected_book.isbn, book_status="Available").distinct('library')
    available_copies = Book.objects.filter(
        isbn=selected_book.isbn, book_status="Available").count()
    context = {
        'book': selected_book,
        'books': books,
        'available_copies': available_copies,
    }
    user = request.user
    if user.is_authenticated:
        reserved_items = Reserve.objects.filter(
            reserve_status='active', user=user)
        context.update({'reserved_items': reserved_items})
    if request.method == 'POST':
        reserve_limit = user.rule.reserve_limit
        reserve_book_id = request.POST.get('reservebookid', 'not_selected')
        match reserve_book_id:
            case 'not_selected':
                messages.error(request, 'Please select your option before clicking the button.')
            case _:
                reserve_book = Book.objects.get(id=reserve_book_id)
                user_reserve_number = reserved_items.count()
                if user_reserve_number < reserve_limit:
                    new_reserve = Reserve(
                       reserve_date=timezone.datetime.now(), user=request.user, book=reserve_book)
                    reserve_book.book_status = "Reserved"
                    reserve_book.save()
                    new_reserve.save()
                    messages.success(
                        request, 'You have reserved this book successfully')
                else:
                    messages.error(
                    request, 'You have reached your reserve limit. Cannot reserve.')
        return redirect('book', book_id)

    return render(request, 'books/book.html', context)


def search(request):
    """
    Handle search queries for books based on various criteria.

    Filters books based on keywords, title, library district, author, and publisher.
    Renders the 'search.html' template with the filtered books and search parameters.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML page with search results.
    """
    queryset_list = Book.objects.all()
    # print("District Choices:", district_choices)  # Debugging output
    # print("Request GET:", request.GET)  # Check what values are being sent
    # Rest of your filtering logic...
    if 'keywords' in request.GET:  # check if existence of key words in search
        # if words entered, put such words into "keywords"
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(
                description__icontains=keywords  # icontains means case insensitive
            )
    if 'title' in request.GET:  # check if existence of key words in search
        title = request.GET['title']  # if words entered, put such words into
        if title:
            queryset_list = queryset_list.filter(
                title__icontains=title  # words contained are fine
            )
    if 'library' in request.GET:
        library = request.GET['library']
        if library:
            queryset_list = queryset_list.filter(
                library__district__iexact=library  # Assuming 'district' is the field in Library
            )
    if 'author' in request.GET:  # check if existence of key words in search
        author = request.GET['author']  # if words entered, put such words into
        if author:
            queryset_list = queryset_list.filter(
                author__icontains=author  # words contained are fine
            )
    if 'publisher' in request.GET:  # check if existence of key words in search
        # if words entered, put such words into
        publisher = request.GET['publisher']
        if publisher:
            queryset_list = queryset_list.filter(
                publisher__icontains=publisher  # words contained are fine
            )
    context = {
        'district_choices': district_choices,
        'status_choices': status_choices,
        'books': queryset_list,
        'values': request.GET
    }
    return render(request, 'books/search.html', context)
