from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('article/', views.article, name='article'),
    path('lexique/', views.lexique, name='lexique'),
]