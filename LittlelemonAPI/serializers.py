from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category,MenuItem, Cart, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','slug','title']

class MenuItemSerializer(serializers.ModelSerializer):
    category=CategorySerializer()
    class Meta:
        model=MenuItem
        fields=['id', 'title', 'price', 'featured', 'category']



class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']

class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price', 'price']

class OrderSerializer(serializers.ModelSerializer):
    delivery_crew=serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    order_items=OrderItemSerializer(many=True,read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items']
        
class AllManagerSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['id','username','email']