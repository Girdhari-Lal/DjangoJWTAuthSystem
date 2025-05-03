from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.views import APIView
from users.serializers import UserRegisterSerializer, UserLoginSerializer, UserProfileSerializer
from django.contrib.auth import authenticate
from users.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated 
# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegisterView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'Message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response({
            'Message': 'User not created',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email = email, password = password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'Message': 'Login Success'}, status = status.HTTP_200_OK)
            else:
                return Response({'Error' : 'Email or password is not valid'}, status = status.HTTP_404_NOT_FOUND)
                
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status = status.HTTP_200_OK)  
    
  