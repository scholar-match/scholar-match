from django.shortcuts import render

# Create your views here.
# todo/views.py

from django.shortcuts import render
from rest_framework import viewsets          
from .serializers import ScholarMatchSerializer      
from .models import ScholarMatch                     

class ScholarMatchView(viewsets.ModelViewSet):       
    serializer_class = ScholarMatchSerializer          
    queryset = ScholarMatch.objects.all()              
