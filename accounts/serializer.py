from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


from rest_framework import serializers

from accounts.models import NanumUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        exclude = ('password', )


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = '__all__'


class NanumUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = NanumUser
        fields = ('user', 'birthday', 'profile_image')


class NanumCreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = NanumUser
        fields = ('birthday', 'profile_image')

