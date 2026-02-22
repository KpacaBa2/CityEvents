from django.urls import path

from apps.tickets import views

urlpatterns = [
    path('my/', views.my_tickets, name='my'),
]
