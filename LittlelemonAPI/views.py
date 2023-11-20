from django.shortcuts import render
from rest_framework import generics

class MenuItemPageView(generics.ListCreateAPIView):
    