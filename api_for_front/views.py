from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response


class test(APIView):
    def get(self, request):
        return Response({'ds': 'as'})
