from django.urls import path
from .views import menu_item_list_view

urlpatterns = [
    path('menu-items/', menu_item_list_view, name='menu-item-list'),
    
]
