"""finin_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt import views as jwt_views
from django.contrib.auth import views as auth_view
from allauth.account.views import confirm_email
from allauth.account.views import ConfirmEmailView
from user_login_register.views import CustomConfirmEmailView, ConfirmEmailView, signup, profile, activate, home_view
from django.views.generic.base import TemplateView, TemplateResponseMixin, RedirectView
from . import regex
from rest_auth.registration.views import VerifyEmailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_auth.views import LogoutView

from transaction.views import transaction_view
from rest_framework import routers
from rest_framework.routers import DefaultRouter

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name="home"),
    re_path(r'^transaction/', transaction_view, name="transaction"),
    re_path(r'user_login_register/', include('user_login_register.urls')),
    re_path('auth/', include('rest_framework.urls')),
    path('rest-auth/logout/', LogoutView, name="rest_logout"),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    
    re_path(r'^rest-auth/', include('rest_auth.urls')),
    re_path(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
