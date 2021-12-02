from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializer import UserSerializer, UserProfileSerializer, VehicleSerializer
from rest_framework import response,status
from .models import User,UserProfile,Vehicles
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

    def get(self,request):
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





class VehiclesView(GenericAPIView):
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = VehicleSerializer

    def post(self,request):
        user_data = self.request.user
        print("user_data.id" , user_data.id)
        vehicle = JSONParser().parse(request)
        vehicle['user'] = user_data.id
        vehicle_serializer = VehicleSerializer(data=vehicle)
        if vehicle_serializer.is_valid():
            vehicle_serializer.save()
            return JsonResponse(vehicle_serializer.data,
                                status=201)
        return JsonResponse(vehicle_serializer.errors,
                            status=400)

    def get(self,request):
        data = Vehicles.objects.all()
        serializer = VehicleSerializer(data, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def put(self,request):
        requestData = JSONParser().parse(request)
        print("self.request.user.id",self.request.user.id)
        vehicleData= Vehicles.objects.get(user=self.request.user.id, model=requestData['model'])
        print("vehicleData", vehicleData)
        serializer = VehicleSerializer(instance=vehicleData, data=requestData, partial=True)
        if serializer.is_valid():
            # print(serializer.validated_data)
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
