from django.urls import path

from apps.categories import views

urlpatterns = [
    path('', views.category_list, name='list'),
    path('create/', views.CategoryCreateView.as_view(), name='create'),
    path('<slug:slug>/', views.category_detail, name='detail'),
    path('<slug:slug>/edit/', views.CategoryUpdateView.as_view(), name='edit'),
    path('<slug:slug>/delete/', views.CategoryDeleteView.as_view(), name='delete'),
]
