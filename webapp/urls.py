from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('article/<slug:slug>/', views.article, name='article'),
    path('categorie/<slug:slug>/', views.category, name='category'),
    path('lexique/', views.lexique, name='lexique'),
]