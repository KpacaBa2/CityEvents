from django.urls import path

from apps.api import views

urlpatterns = [
    path('events/', views.events_collection, name='events_collection'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    path('categories/', views.categories_list, name='categories'),
    path('venues/', views.venues_list, name='venues'),
    path('reviews/', views.reviews_list, name='reviews'),
]
