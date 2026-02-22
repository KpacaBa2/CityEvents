from django.urls import path

from apps.reviews import views

urlpatterns = [
    path('<slug:slug>/add/', views.add_review, name='add'),
]
