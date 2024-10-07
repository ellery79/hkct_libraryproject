from django.shortcuts import render
from books.models import Book
from libraries.models import Library
from accounts.models import Rule


# Create your views here.
def index(request):
    random3_books_query_set = Book.objects.filter(is_latest=True).order_by('?')[0:3]
    context = {'random3_books_list': random3_books_query_set}
    return render(request, 'pages/index.html', context)

def about(request):
    library_query_set = Library.objects.all()
    central_library = Library.objects.get(id=1)
    kowloon_library = Library.objects.get(id=3)
    new_Territories_library = Library.objects.get(id=2)
    default_rule = Rule.objects.get(rule_name="default")
    context = {'library_list': library_query_set,
               'central':central_library,
               'kowloon':kowloon_library,
               'nt':new_Territories_library,
               'default_rule':default_rule}
    return render(request, 'pages/about.html', context)