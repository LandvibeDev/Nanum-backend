from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

from accounts.views import NanumUserViewSet

user_router = routers.DefaultRouter()
user_router.register(r'users', NanumUserViewSet, base_name='user')