from django.urls import path
from . import views

urlpatterns = [
    path('', views.books, name='books'),
    path('books/<int:book_id>/', views.book, name='book'),  # Updated to only use book_id
    path('search', views.search, name='search'),
]