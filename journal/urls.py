from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new/', views.new_entry, name='new_entry'),
    path('edit/<int:pk>/', views.edit_entry, name='edit_entry'),
]
