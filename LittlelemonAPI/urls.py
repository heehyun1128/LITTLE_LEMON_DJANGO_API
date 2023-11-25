from django.urls import path,include
from .views import login_view,customer_register_view,menu_items_pagination,menu_items_by_category_view,menu_item_list_view,menu_item_detail_view,category_view, all_managers_view,manage_delivery_crew_view,delivery_crew_remove_view,cart_view,order_view,single_order_view,sort_menu_by_price
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login/', login_view, name='login_view'),
    path('register/', customer_register_view, name='customer_register_view'),
    path('menu-items/', menu_item_list_view, name='menu-item-list'),
    path('menu-items/sort=price',sort_menu_by_price , name='menu-item-sort-by-price'),
    path('menu-items/<int:pk>', menu_item_detail_view, name='menu-items'),
    path('menu-items/category/<int:category_id>/', menu_items_by_category_view, name='menu_items_by_category'),
    path('menu-items/paginated/', menu_items_pagination, name='menu_items_pagination'),
    path('groups/manager/users', all_managers_view, name='manager_list'),
    path('groups/delivery-crew/users', manage_delivery_crew_view, name='delivery_crew'),
    path('groups/delivery-crew/users/<int:pk>', delivery_crew_remove_view, name='delivery_crew_remove'),
    path('category', category_view, name='category_view'),
    path('cart/menu-items', cart_view, name='cart_view'),
    path('orders', order_view, name='order_view'),
    path('orders/<int:pk>', single_order_view, name='single_order_view'),
    # path('secret',secret),
    path('api-token-auth/',obtain_auth_token)
    
]
