from django.urls import path,include
from .views import menu_item_list_view,menu_item_detail_view,all_managers_view,secret
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items/', menu_item_list_view, name='menu-item-list'),
    path('menu-items/<int:pk>', menu_item_detail_view, name='menu-items'),
    path('groups/manager/users', all_managers_view, name='manager_list'),
    path('secret',secret),
    path('api-token-auth/',obtain_auth_token)
    
]
