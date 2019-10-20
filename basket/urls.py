from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('create/', views.BasketView.as_view(action_name="create"), name="create"),
    path('<int:pk>/', views.BasketView.as_view(action_name="get"), name="get"),
    path('<int:pk>/add-item/',views.BasketView.as_view(action_name="add_item"), name="add-item"),
    path('<int:pk>/remove-item/',views.BasketView.as_view(action_name="remove_item"), name="remove-item"),
    path('<int:pk>/empty/', views.BasketView.as_view(action_name="empty"), name="empty"),
]
