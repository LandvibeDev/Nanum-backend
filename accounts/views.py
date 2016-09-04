from logging import warning
from django.contrib.auth import (
    get_user_model, login as auth_login
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.sessions.models import Session

from rest_framework import parsers, renderers
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import NanumUser
from accounts.serializer import NanumUserSerializer, NanumCreateUserSerializer
from study.models import Study, StudyMember

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
        user = get_object_or_404(get_user_model(), username=username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((AllowAny,))
def info_account(request, user_pk=None, format=None):
    if request.method == 'GET':
        user = get_object_or_404(NanumUser, user_id=user_pk)
        serializer = NanumUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@login_required(login_url='/accounts/login-ui/')
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
            # StudyMember 인스턴스 리스트 얻기
            study_member = nanum_user.members.all()
            study_list = []
            # StudyMember 에서 각 Study 인스턴스의 정보를 사전형으로 만든 뒤 리스트에 추가
            for sm in study_member:
                study_dic = {'id': sm.id, 'title': sm.title, 'topic': sm.topic}
                study_list.append(study_dic)

            # user 정보와 user 와 관련된 study 정보를 하나의 사전형으로 만듬
            user_study_info = {'study_info': study_list,
                               'user_info': NanumUserSerializer(nanum_user).data}
            # 위의 정보를 JSON 형식으로 반환
            return JsonResponse(user_study_info)

            # return Response(NanumUserSerializer(nanum_user).data)

        return super(NanumUserViewSet, self).retrieve(request, pk)


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
        auth_login(request, user) # save session
        return Response({'token': token.key,'sessionid': request.session.session_key}, status=status.HTTP_200_OK)

obtain_auth_token = ObtainAuthToken.as_view()


@api_view(['POST'])
@permission_classes((AllowAny,))
def check_session(request, format=None):
    if request.method == 'POST':
        s = Session.objects.filter(pk=request.POST['sessionid'])
        #s = Session.objects.filter(pk=request.session.session_key)
        if s.exists():
            return Response({"Session Success": "Session is exist"}, status=status.HTTP_200_OK)
        else:
            return Response({"Session Fail": "Session is expire or not exist"}, status=status.HTTP_401_UNAUTHORIZED)

