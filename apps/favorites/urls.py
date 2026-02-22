from django.urls import path

from apps.favorites import views

urlpatterns = [
    path('', views.favorite_list, name='list'),
    path('<slug:slug>/toggle/', views.toggle_favorite, name='toggle'),
]
