from django.urls import path
from jobs.views import job_search

from .views import signout_user, signup_user, signin_user

urlpatterns = [
    path('sign-up/', signup_user, name='signup_user'),
    path('sign-in/', signin_user, name='signin_user'),
    path('sign-out/', signout_user, name='signout_user'),
]
