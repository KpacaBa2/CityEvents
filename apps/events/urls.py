from django.urls import path

from apps.events import views

urlpatterns = [
    path('', views.event_list, name='list'),
    path('create/', views.EventCreateView.as_view(), name='create'),
    path('<slug:slug>/', views.event_detail, name='detail'),
    path('<slug:slug>/edit/', views.EventUpdateView.as_view(), name='edit'),
    path('<slug:slug>/delete/', views.EventDeleteView.as_view(), name='delete'),
]
