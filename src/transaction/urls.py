from django.urls import path, re_path
from . import views


app_name = 'transaction'

urlpatterns = [
    re_path('', views.test_view, name="test"),
]