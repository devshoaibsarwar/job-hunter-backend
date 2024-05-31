import jwt

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import fetch_email

from django.conf import settings
from django.db import transaction
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password


from .models import User
from .serializers import (
    SignupSerializer,
    SigninSerializer,
)

@transaction.atomic
@api_view(['POST'])
def signup_user(request):
    user_data = request.data

    if not user_data:
        return Response({'message': 'Payload not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    email = user_data.get('email')
    password = user_data.get('password')
    
    if not email:
        return Response({'message': 'Email param is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not password:
        return Response({'message': 'Password param is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        return Response({'message': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        pass

    encrypted_password = make_password(password)

    user_info = {
        'email': email,
        'password': encrypted_password
    }

    user_serializer = SignupSerializer(data=user_info)

    if user_serializer.is_valid():
        user = user_serializer.save()
        
        payload = {
            'user_id': user.id,
            'email': user.email
        }
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')

        response_data = {
            'message': 'User created successfully',
            'token': token,
            'user': user_serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def signin_user(request):
    user_data = request.data

    if not user_data:
        return Response({'message': 'User data is required'}, status=status.HTTP_400_BAD_REQUEST)

    signin_serializer = SigninSerializer(data=user_data)
    if not signin_serializer.is_valid():
        return Response(signin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = user_data.get('email')
    password = user_data.get('password')

    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except MultipleObjectsReturned:
        return Response({'message': 'Multiple users found with this email'}, status=status.HTTP_400_BAD_REQUEST)

    if not check_password(password, user.password):
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    payload = {
        'user_id': user.id,
        'email': user.email
    }

    token = jwt.encode(payload, key=settings.JWT_SECRET, algorithm='HS256')
    user.api_token = token
    user.save()

    user_data = {
        'email': user.email,
        'api_token': token
    }

    response_data = {
        'message': 'Signin successful',
        'user': user_data
    }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def signout_user(request):
    bearer_token = request.headers['Authorization']
    email = fetch_email(bearer_token)
    
    try:
        user = User.objects.get(email=email)
        user.api_token = None
        user.save()

        response = { 'message': 'Signout Successfull' }
        return Response(response, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        response = { 'message': 'User not found' }
        return Response(response, status=status.HTTP_404_NOT_FOUND)
