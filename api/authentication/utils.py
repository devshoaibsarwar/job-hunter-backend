import jwt
from django.conf import settings

def fetch_email(bearer_token):
    token_without_bearer = bearer_token.split()[1] 
    payload = jwt.decode(token_without_bearer, settings.JWT_SECRET, algorithms=['HS256'])
    return payload['email']
