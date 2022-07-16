from django.urls import path
from .views import lime_respostas, lista_participantes, sessao

urlpatterns = [
    path('responses/<str:sid>/', lime_respostas, name='responses'),
    path('participants/<str:sid>/', lista_participantes, name='participants'),
    path('session/', sessao, name='session'),
]