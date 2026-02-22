from django.urls import path

from apps.tags import views

urlpatterns = [
    path('', views.tag_list, name='list'),
]
