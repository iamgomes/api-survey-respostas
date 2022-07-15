from django.urls import path
from .views import lime_respostas

urlpatterns = [
    path('responses/<str:sid>/', lime_respostas, name='responses'),
]