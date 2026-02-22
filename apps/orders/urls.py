from django.urls import path

from apps.orders import views

urlpatterns = [
    path('my/', views.my_orders, name='my'),
]
