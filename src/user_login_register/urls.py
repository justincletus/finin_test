from django.urls import path, re_path
from django.conf.urls import url
from . import views


app_name = 'user_login_register'

urlpatterns = [
    # path('', views.home_view, name="home"),
    re_path('refresh/', views.createTokenUser, name="user_token"),
    re_path(r'signup/', views.signup, name="user_register"),

]