from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book-list'),
    path('add/', views.book_create, name='book-create'),
    path('edit/<int:book_id>/', views.book_edit, name='book-edit'),
    path('delete/<int:book_id>/', views.book_delete, name='book-delete'),
]