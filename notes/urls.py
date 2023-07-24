# notes/urls.py
from django.urls import path
from .views import NoteAPIView

urlpatterns = [
    path('notes/', NoteAPIView.as_view()),
    path('notes/<int:pk>/', NoteAPIView.as_view()),
]
 