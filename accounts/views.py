from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash, authenticate
)
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import *
from rest_framework.authtoken.models import Token

from accounts.models import NanumUser
from accounts.serializer import NanumUserSerializer, NanumCreateUserSerializer, UserSerializer



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
def delete_account(request, username=None, format=None):
    if request.method == 'DELETE':
        user = get_object_or_404(get_user_model(),username=username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((AllowAny,))
def info_account(request, user_pk=None, format=None):
    if request.method == 'GET':
        user = get_object_or_404(NanumUser, user_id=user_pk)
        serializer = NanumUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@login_required(login_url='/accounts/login/')
def first_page(request):
    return redirect('/study/')




class NanumUserViewSet(viewsets.ModelViewSet):
    queryset = NanumUser.objects.all()
    serializer_class = NanumUserSerializer

    def retrieve(self, request, pk=None):
        if pk == 'i':
            token = request.META['HTTP_AUTHORIZATION']
            user_by_token = Token.objects.get(key=token[6:]).user
            nanum_user = NanumUser.objects.get(user=user_by_token)
            # user = User.objects.get(auth_token=token[6:])
            # auth_user = authenticate(username=user.username, password=user.password)
            # auth_login(request, auth_user)
            return Response(NanumUserSerializer(nanum_user).data)
        return super(NanumUserViewSet, self).retrieve(request, pk)



from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        auth_login(request, user)
        return Response({'token': token.key})


obtain_auth_token = ObtainAuthToken.as_view()
