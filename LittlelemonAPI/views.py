from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Category,MenuItem, Cart, Order, OrderItem
from .serializers import CustomerRegisterSerializer, MenuItemSerializer, CategorySerializer,AllManagerSerializer,CartSerializer,CartAddSerializer,CartRemoveSerializer,OrderSerializer,OrderItemSerializer,OrderPutSerializer
from django.http import JsonResponse, HttpResponseBadRequest
from .permissions import IsManager
from django.shortcuts import get_object_or_404
import math
from datetime import date
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes([AllowAny]) 
def customer_register_view(request):
    if request.method=='POST':
        serializer=CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([])
def login_view(request):
    username=request.data.get('username')
    password=request.data.get('password')
    
    user=authenticate(request,username=username,password=password)
    
    if user is not None:
        login(request,user)
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

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

# sort menu items
@api_view(['GET'])
def sort_menu_by_price(request):
    menu_items=MenuItem.objects.order_by('price')
    serializer=MenuItemSerializer(menu_items,many=True)
    return Response(serializer.data)
    
    
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


@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def menu_item_detail_view(request, pk):
    try:
        menu_item=MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Menu Item Not Found!'})
    if request.method=='GET':
        serializer=MenuItemSerializer(menu_item)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method=='PUT':
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response(data={'message': 'Access Denied'}, status=403)
        try:
            menu_item=MenuItem.objects.first()
        except menu_item.DoesNotExist:
            return Response(data={'message': 'Item of the day not found'}, status=404)
        serializer=MenuItemSerializer(menu_item,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'message': 'Item of the day updated successfully'}, status=200)
        else:
            return Response(data={'message': 'Invalid data'}, status=400)
           

    elif request.method=='DELETE':
        if request.user.is_staff:
            menu_item.delete()
            return Response(data={'message': 'Menu Item Deleted Successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': 'Access Denied'}, status=status.HTTP_403_FORBIDDEN)
            
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated, IsManager | IsAdminUser])
def all_managers_view(request, pk=None):
    if request.method=='GET':
        if pk:
            user=get_object_or_404(User,pk=pk)
            managers = Group.objects.get(name='manager')
            if user in managers.user_set.all():
                serializer=AllManagerSerializer(user)
                return Response(serializer.data)
            else:
                return Response({'message':'User not found'},status=status.HTTP_404_NOT_FOUND)
        queryset = User.objects.filter(groups__name='manager') #__ to traverse relationships between models
        serializer = AllManagerSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        username=request.data.get('username')
        if username:
            user=get_object_or_404(User,username=username)
            managers = Group.objects.get(name='manager')
            managers.user_set.add(user)
            return Response({'message': 'User added to Managers group'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsManager | IsAdminUser])
def managers_remove_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    managers = Group.objects.get(name='Managers')
    managers.user_set.remove(user)
    return JsonResponse(status=200, data={'message': 'User removed from Managers group'})


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def manage_delivery_crew_view(request,pk=None):
    if request.method=='GET':
        queryset=User.objects.filter(groups__name='delivery_crew')
        return Response({'crew_members': [user.username for user in queryset]})
    elif request.method=='POST':
        username=request.data.get('username')
        if username:
            user=get_object_or_404(User,username=username)
            crew=Group.objects.get(name='delivery_crew')
            crew.user_set.add(user)
            return Response({'message': 'User added to Delivery Crew group'}, status=201)
    return Response({'message': 'Invalid request method'}, status=400)
        
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
@permission_classes([IsAuthenticated])
def order_view(request):
    if request.method == 'GET':
        if request.user.groups.filter(name='manager').exists() or request.user.is_superuser:
            query=Order.objects.all()
        elif request.user.groups.filter(name='delivery_crew').exists():
            query = Order.objects.filter(delivery_crew=request.user)
        else:
            query = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(query, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        cart = Cart.objects.filter(user=request.user)
        if not cart.exists():
            return Response({'message': 'Bad Request'}, status=400)
        
        total = math.fsum([float(item.price) for item in cart])
        order = Order.objects.create(user=request.user, status=False, total=total, date=date.today())
        
        for item in cart:
            menuitem = get_object_or_404(MenuItem, id=item.menuitem_id)
            order_item = OrderItem.objects.create(order=order, menuitem=menuitem, quantity=item.quantity)
            order_item.save()
        
        cart.delete()
        return Response({'message': f'Your order has been placed! Your order number is {order.id}'},status=201)
    return Response({'message': 'Invalid request method'}, status=400)
    

@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def single_order_view(request, pk=None):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'GET':
        order_serializer = OrderSerializer(order)
        query = OrderItem.objects.filter(order=order)
        order_items_serializer = OrderItemSerializer(query, many=True)
        response_data = {
            'order': {
                **order_serializer.data,
                'order_items': order_items_serializer.data}
        }

        return Response(response_data)

    elif request.method == 'PATCH':
        order = Order.objects.get(pk=pk)
        order.status = not order.status
        order.save()
        return Response(data={'message': f'Status of order #{order.id} changed to {order.status}'},status=200)

    elif request.method == 'PUT':
        serialized_item = OrderPutSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        crew_pk = request.data['delivery_crew']
        
        crew = get_object_or_404(User, pk=crew_pk)
        order.delivery_crew = crew
        order.save()
        return Response({'message': f'{crew.username} was assigned to order #{order.id}'},status=201)

    elif request.method == 'DELETE':
        order = Order.objects.get(pk=pk)
        order_number = order.id
        order.delete()
        return Response( data={'message': f'Order #{order_number} was deleted'},status=200)
    return Response({'message': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)