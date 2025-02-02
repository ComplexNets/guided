from django.urls import path
from . import views

app_name = 'guided_writing'

urlpatterns = [
    path('programs/', views.program_list, name='program_list'),
    path('program/<int:program_id>/start/', views.start_program, name='start_program'),
    path('program/<int:program_id>/session/<int:session_number>/', views.guided_session, name='guided_session'),
]
