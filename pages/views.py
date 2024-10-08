"""
Views for the main pages of the Django project.

This module contains view functions for rendering the index and about pages.
Each view handles fetching necessary data from the database and passing it
to the corresponding template for rendering.
"""

from django.shortcuts import render

from accounts.models import Rule
from books.models import Book
from libraries.models import Library, district_choices


# Create your views here.
def index(request):
    """
    Render the homepage with a selection of the latest books and district choices.

    This view retrieves a random selection of three latest books and includes
    district choices to be displayed on the homepage.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered index page with context data.
    """
    books = Book.objects.filter(is_latest =True).order_by('?')[:3]
    context = {
        'books': books,
        'district_choices': district_choices  # Add district_choices to context
    }
    return render(request, 'pages/index.html', context)


def about(request):
    """
    Render the about page with library information and default rules.

    This view gathers all libraries, specific central libraries by ID, and the
    default rule to display detailed information on the about page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered about page with context data.
    """
    library_query_set = Library.objects.all()
    central_library = Library.objects.get(id=1)
    kowloon_library = Library.objects.get(id=3)
    new_Territories_library = Library.objects.get(id=2)
    default_rule = Rule.objects.get(rule_name="default")
    context = {'library_list': library_query_set,
               'central': central_library,
               'kowloon': kowloon_library,
               'nt': new_Territories_library,
               'default_rule': default_rule}
    return render(request, 'pages/about.html', context)
