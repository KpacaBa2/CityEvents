from django.urls import path

from apps.organizers import views

urlpatterns = [
    path('', views.organizer_list, name='list'),
    path('<slug:slug>/', views.organizer_detail, name='detail'),
]
