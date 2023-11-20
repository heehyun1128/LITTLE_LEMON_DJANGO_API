from django.urls import path
from .views import menu_item_list_view,menu_item_detail_view

urlpatterns = [
    path('menu-items/', menu_item_list_view, name='menu-item-list'),
    path('menu-items/<int:pk>', menu_item_detail_view, name='menu-item-list'),
    
]
