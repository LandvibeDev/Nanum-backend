from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets

from accounts.models import NanumUser
from accounts.serializer import NanumUserSerializer, NanumCreateUserSerializer


@api_view(['GET', 'POST'])
def join(request, format=None):
    if request.method == 'POST':
        userform = UserCreationForm(request.POST)
        if userform.is_valid():
            userform.save()

            # TODO test required
            nanum_user_serializer = NanumCreateUserSerializer(data=request.data)
            if nanum_user_serializer.is_valid():
                nanum_user_serializer.save(user=userform.instance)
            return Response(userform.data, status=status.HTTP_201_CREATED)
        return Response(userform.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        userform = UserCreationForm()
        return render(
            request, 'signup.html',
            {
                'userform' : userform,
            }
        )


@api_view(['DELETE'])
def delete_account(request, username=None, format=None):
    if request.method == 'DELETE':
        User = get_user_model()
        user = get_object_or_404(User, username=username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


