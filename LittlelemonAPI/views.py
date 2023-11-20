from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Category,MenuItem, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, CategorySerializer,AllManagerSerializer,CartSerializer,CartAddSerializer,CartRemoveSerializer,OrderSerializer,OrderItemSerializer,OrderPutSerializer
from django.http import JsonResponse, HttpResponseBadRequest
from .permissions import IsManager
from django.shortcuts import get_object_or_404
import math
from datetime import date

@api_view()
def secret(request):
    return Response({"message":"secret"})

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def menu_item_list_view(request):
    if request.method=='GET':
        queryset=MenuItem.objects.all()
        serializer=MenuItemSerializer(queryset,many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        if not request.user.is_staff:
            return Response({'error':'You do not have the authorization to perform this action.'},status=status.HTTP_403_FORBIDDEN)
        
        serializer=MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def category_view(request):
    if request.method=='GET':
        queryset=Category.objects.all()
        serializer=CategorySerializer(queryset,many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        if not request.user.is_staff:
            return Response({'error':'You do not have the authorization to perform this action.'},status=status.HTTP_403_FORBIDDEN)
        
        serializer=CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def menu_item_detail_view(request, pk):
    try:
        menu_item=MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return JsonResponse(status=404,data={'message':'Menu Item Not Found!'})
    if request.method=='GET':
        serializer=MenuItemSerializer(menu_item)
        return JsonResponse(status=200,data=serializer.data)
    elif request.method=='PATCH':
        if request.user.is_staff or (request.user.is_authenticated and request.user.is_manager):
            menu_item.featured=not menu_item.featured
            menu_item.save()
            return JsonResponse(status=200,data={'message':'Featured status changed'})
        else:
            return JsonResponse(status=403,data={'message':'Access Denied'})
    elif request.method=='DELETE':
        if request.user.is_staff:
            menu_item.delete()
            return JsonResponse(status=200,data={'message':'Menu Item Deleted Successfully.'})
        else:
            return JsonResponse(status=403,data={'message':'Access Denied'})
            
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated, IsManager | IsAdminUser])
def all_managers_view(request, pk=None):
    if request.method=='GET':
        if pk:
            user=get_object_or_404(User,pk=pk)
            managers = Group.objects.get(name='manager')
            if user in managers.user_set.all():
                serializer=AllManagerSerializer(user)
                return JsonResponse(data=serializer.data)
            else:
                return JsonResponse(status=404,data={'message':'User not found'})
        queryset = User.objects.filter(groups__name='manager') #__ to traverse relationships between models
        serializer = AllManagerSerializer(queryset, many=True)
        return JsonResponse(data=serializer.data)
    elif request.method=='POST':
        username=request.data.get('username')
        if username:
            user=get_object_or_404(User,username=username)
            managers = Group.objects.get(name='manager')
            managers.user_set.add(user)
            return JsonResponse(status=201, data={'message': 'User added to Managers group'})
        return JsonResponse(status=400, data={'message': 'Invalid data'})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsManager | IsAdminUser])
def managers_remove_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    managers = Group.objects.get(name='Managers')
    managers.user_set.remove(user)
    return JsonResponse(status=200, data={'message': 'User removed from Managers group'})


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def manage_delivery_crew_view(request,pk=None):
    if request.method=='POST':
        username=request.data.get('username')
        if username:
            user=get_object_or_404(User,username=username)
            crew=Group.objects.get(name='delivery_crew')
            crew.user_set.add(user)
            return JsonResponse(status=201, data={'message': 'User added to Delivery Crew group'})
        
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsManager | IsAdminUser])
def delivery_crew_remove_view(request, pk):
    user=get_object_or_404(User,pk=pk)
    crew=Group.objects.get(name='delivery_crew')
    crew.user_set.remove(user)
    return JsonResponse(status=200, data={'message': 'User removed from the Delivery crew group'})


@api_view(['GET', 'POST', 'DELETE'])
def cart_view(request, *args, **kwargs):
    if request.method=='GET':
        cart=Cart.objects.filter(user=request.user)
        serializer=CartSerializer(cart,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serialized_item=CartAddSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        id=request.data['menuitem']
        quantity=request.data['quantity']
        item = get_object_or_404(MenuItem, id=id)
        price=item.price*int(quantity)
        
        try:
            Cart.objects.create(user=request.user,quantity=quantity,unit_price=item.price, price=price, menuitem_id=id)
        except:
            return JsonResponse(status=409, data={'message':'Item already in cart'})
        return JsonResponse(status=201, data={'message':'Item added to cart!'})
    elif request.method == 'DELETE':
        if request.data['menuitem']:
            serialized_item=CartRemoveSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            menuitem=request.data['menuitem']
            cart = get_object_or_404(Cart, user=request.user, menuitem=menuitem)
            cart.delete()
            return JsonResponse(status=200, data={'message':'Item removed from cart'})
        else:
            Cart.objects.filter(user=request.user).delete()
            return JsonResponse(status=201, data={'message':'All items removed from cart'})
        
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsManager | IsAdminUser])
def order_view(request):
    if request.method == 'GET':
        if request.user.group.filter(name='manager').exist() or request.user.is_superuser:
            query=Order.objects.all()
        elif request.user.groups.filter(name='delivery_crew').exists():
            query = Order.objects.filter(delivery_crew=request.user)
        else:
            query = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(query, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        cart = Cart.objects.filter(user=request.user)
        if not cart.exists():
            return HttpResponseBadRequest()
        
        total = math.fsum([float(item.price) for item in cart])
        order = Order.objects.create(user=request.user, status=False, total=total, date=date.today())
        
        for item in cart:
            menuitem = get_object_or_404(MenuItem, id=item.menuitem_id)
            order_item = OrderItem.objects.create(order=order, menuitem=menuitem, quantity=item.quantity)
            order_item.save()
        
        cart.delete()
        return JsonResponse(status=201, data={'message': f'Your order has been placed! Your order number is {order.id}'})
    

@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsManager | IsAdminUser])
def single_order_view(request, pk=None):
    if request.method == 'GET':
        query = OrderItem.objects.filter(order_id=pk)
        serializer = OrderItemSerializer(query, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PATCH':
        order = Order.objects.get(pk=pk)
        order.status = not order.status
        order.save()
        return JsonResponse(status=200, data={'message': f'Status of order #{order.id} changed to {order.status}'})

    elif request.method == 'PUT':
        serialized_item = OrderPutSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        crew_pk = request.data['delivery_crew']
        order = get_object_or_404(Order, pk=pk)
        crew = get_object_or_404(User, pk=crew_pk)
        order.delivery_crew = crew
        order.save()
        return JsonResponse(status=201, data={'message': f'{crew.username} was assigned to order #{order.id}'})

    elif request.method == 'DELETE':
        order = Order.objects.get(pk=pk)
        order_number = order.id
        order.delete()
        return JsonResponse(status=200, data={'message': f'Order #{order_number} was deleted'})