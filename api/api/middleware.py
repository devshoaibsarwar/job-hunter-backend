import jwt
from rest_framework import status

from django.http import JsonResponse
from authentication.utils import fetch_email
from authentication.models import User


class TokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        AUTH_PREFIX = '/auth/'
        excluded_urls = [f'{AUTH_PREFIX}sign-up/', f'{AUTH_PREFIX}sign-in/']
 
        if request.path_info in excluded_urls:
            return self.get_response(request)
        
        if 'Authorization' not in request.headers:
            response = {'message': 'Token is missing'}
            return JsonResponse(response, status=status.HTTP_401_UNAUTHORIZED)

        bearer_token = request.headers['Authorization']


        try:
            email = fetch_email(bearer_token)

            user = User.objects.get(email=email)

            if not user.api_token:
                response = {'message': 'Token is invalid'}
                return JsonResponse(response, status=status.HTTP_401_UNAUTHORIZED)    

        except jwt.ExpiredSignatureError:
            response = {'message': 'Token expired'}
            return JsonResponse(response, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            response = {'message': 'Invalid token'}
            return JsonResponse(response, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            response = {'message': 'User not found'}
            return JsonResponse(response, status=status.HTTP_404_NOT_FOUND)

        print(request.path_info)
        response = self.get_response(request)
        return response