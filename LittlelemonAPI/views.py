from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Category,MenuItem, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, CategorySerializer,AllManagerSerializer
from django.http import JsonResponse
from .permissions import IsManager
from django.shortcuts import get_object_or_404

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
            
@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated, IsManager | IsAdminUser])
def all_managers_view(request, pk=None):
    if request.method=='GET':
        if pk:
            user=get_object_or_404(User,pk=pk)
            managers = Group.objects.get(name='Managers')
            if user in managers.user_set.all():
                serializer=AllManagerSerializer(user)
                return JsonResponse(data=serializer.data)
            else:
                return JsonResponse(status=404,data={'message':'User not found'})
        queryset = User.objects.filter(groups__name='Managers') #__ to traverse relationships between models
        serializer = AllManagerSerializer(queryset, many=True)
        return JsonResponse(data=serializer.data)
    elif request.method=='POST':
        username=request.data.get('username')
        if username:
            user=get_object_or_404(User,username=username)
            managers = Group.objects.get(name='Managers')
            managers.user_set.add(user)
            return JsonResponse(status=201, data={'message': 'User added to Managers group'})
        return JsonResponse(status=400, data={'message': 'Invalid data'})
    elif request.method == 'DELETE':
        if pk:
            user = get_object_or_404(User, pk=pk)
            managers = Group.objects.get(name='Managers')
            managers.user_set.remove(user)
            return JsonResponse(status=200, data={'message': 'User removed from Managers group'})
        return JsonResponse(status=400, data={'message': 'Invalid request'})