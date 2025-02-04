from django.urls import path
from . import views

app_name = 'journal'

urlpatterns = [
    path('', views.home, name='home'),
    path('entry/new/', views.new_entry, name='entry_new'),
    path('entry/<int:pk>/edit/', views.edit_entry, name='entry_edit'),
    path('entry/<int:pk>/delete/', views.delete_entry, name='entry_delete'),
    path('profile/', views.profile, name='profile'),
]
