from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category,MenuItem, Cart, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    category=CategorySerializer()
    class Meta:
        model=MenuItem
        fields = '__all__'
        
    def create(self,validated_data):
        category_data=validated_data.pop('category')
        category_instance=Category.objects.create(**category_data)
        menu_item=MenuItem.objects.create(category=category_instance,**validated_data)
        return menu_item
    
    def update(self,instance,validated_data):
        category_data=validated_data.pop('category',None)
        if category_data:
            category_instance=instance.category
            category_serializer=CategorySerializer(category_instance,data=category_data)
            if category_serializer.is_valid():
                category_serializer.save()
        instance = super().update(instance, validated_data)
        return instance



class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']

class CartAddSerializer(serializers.ModelSerializer):
    class Meta():
        model = Cart
        fields = ['menuitem','quantity']
        extra_kwargs = {
            'quantity': {'min_value': 1},
        }
class CartRemoveSerializer(serializers.ModelSerializer):
    class Meta():
        model = Cart
        fields = ['menuitem']
        
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
        
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderPutSerializer(serializers.ModelSerializer):
    class Meta():
        model = Order
        fields = ['delivery_crew']