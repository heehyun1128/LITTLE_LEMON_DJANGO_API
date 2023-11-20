from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Category,MenuItem, Cart, Order, OrderItem
from .serializers import MenuItemSerializer

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


