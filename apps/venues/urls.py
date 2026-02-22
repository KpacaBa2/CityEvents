from django.urls import path

from apps.venues import views

urlpatterns = [
    path('', views.venue_list, name='list'),
    path('create/', views.VenueCreateView.as_view(), name='create'),
    path('<slug:slug>/', views.venue_detail, name='detail'),
    path('<slug:slug>/edit/', views.VenueUpdateView.as_view(), name='edit'),
    path('<slug:slug>/delete/', views.VenueDeleteView.as_view(), name='delete'),
]
