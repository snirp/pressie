from django.contrib.auth.models import User
from django.shortcuts import render
from organisatie.serializers import GebruikerSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics


class GebruikerList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = GebruikerSerializer


class GebruikerDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = GebruikerSerializer
