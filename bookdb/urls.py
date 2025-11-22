from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
    path('search/', views.search, name='search'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('recommendations/<int:pk>/', views.recommendations, name='recommendations_for_book'),
    path('api/', views.api_index, name='api_index'),
    # API
    path('api/books/', views.api_books, name='api_books'),
    path('api/books/<int:pk>/', views.api_book_detail, name='api_book_detail'),
]
