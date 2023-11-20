from django.urls import path,include
from .views import menu_item_list_view,menu_item_detail_view,all_managers_view,secret,manage_delivery_crew_view,delivery_crew_remove_view,cart_view,order_view,single_order_view
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items/', menu_item_list_view, name='menu-item-list'),
    path('menu-items/<int:pk>', menu_item_detail_view, name='menu-items'),
    path('groups/manager/users', all_managers_view, name='manager_list'),
    path('groups/delivery-crew/users', manage_delivery_crew_view, name='delivery_crew'),
    path('groups/delivery-crew/users/<int:pk>', delivery_crew_remove_view, name='delivery_crew_remove'),
    path('cart/menu-items', cart_view, name='cart_view'),
    path('orders', order_view, name='order_view'),
    path('orders/<int:pk>', single_order_view, name='single_order_view'),
    path('secret',secret),
    path('api-token-auth/',obtain_auth_token)
    
]
