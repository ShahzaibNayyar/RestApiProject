from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializer import UserSerializer, UserProfileSerializer
from rest_framework import response,status
from .models import User,UserProfile
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
# Create your views here.

class RegisterUser(GenericAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = UserSerializer
    def post(self,request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self):
        data = UserProfile.objects.all()
        print("data" ,data)
        serializer = UserProfileSerializer(data, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        requestData = JSONParser().parse(request)
        userData = UserProfile.objects.get(user=self.request.user)
        serializer = UserProfileSerializer(instance=userData, data=requestData, partial=True)
        if serializer.is_valid():
            # print(serializer.validated_data)
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get_queryset(self):
        return User.objects.filter(email=self.request.user)

