from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import *

from accounts.models import NanumUser
from accounts.serializer import NanumUserSerializer, NanumCreateUserSerializer


@api_view(['POST'])
@permission_classes((AllowAny,))
def join(request, format=None):
    if request.method == 'POST':
        userform = UserCreationForm(request.POST)
        if userform.is_valid():
            userform.save()
            nanum_user_serializer = NanumCreateUserSerializer(data=request.data)
            if nanum_user_serializer.is_valid():
                nanum_user_serializer.save(user=userform.instance)
            return Response(userform.data, status=status.HTTP_201_CREATED)
        return Response(userform.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes((AllowAny,))
def delete_account(request, user_pk=None, format=None):
    if request.method == 'DELETE':
        user = get_object_or_404(NanumUser, user_id=user_pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((AllowAny,))
def info_account(request, user_pk=None, format=None):
    if request.method == 'GET':
        user = get_object_or_404(NanumUser, user_id=user_pk)
        serializer = NanumUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


