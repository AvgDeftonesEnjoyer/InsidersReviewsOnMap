from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout, get_user_model
from .serializers import RegisterSerializer

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response ({'message' : 'User Created'}, status=201)
        return Response(serializer.errors, status = 400)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password = password)
        if user is not None:
            login(request, user)
            return Response({'message' : 'Login successful'})
        return Response({'error': 'Invalid credentials'}, status = 401)

class LogOutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'Message': 'Logged out'})
    
# Create your views here.
