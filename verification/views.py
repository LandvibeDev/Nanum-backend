from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from logging import warning

from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView

import logging

from verification.models import *
from verification.serializer import *
from accounts.serializer import *
from study.models import Study


# ===================================================
# ============== type 3 : Verificaiton ==============
# ===================================================
@permission_classes((AllowAny,))
class VerificationViewSet(viewsets.ModelViewSet):
    queryset = Verification.objects.all()
    serializer_class = VerificationGetSerializer

    # override : 생성, 수정 시리얼라이저 반환
    def _get_serializer(self, *args, **kwargs):
        serializer_class = VerificationSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # override : verification 인스턴스 생성 후, 해당 인스턴스 반환
    def perform_create(self, serializer):
        return serializer.save()

    # override : Verification 인스턴스 생성 후, 해당 스터디의 멤버 수만큼 인증파일 인스턴스 생성
    def create(self, request, *args, **kwargs):
        serializer = self._get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 1. Verification 인스턴스 생성 후 반환
        verification = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Verification 생성 시 해당 study 와 관련된 member 의 수 만큼 VerificationFile 인스턴스 생성
        # 2. POST 로 넘어오는 board id 에 해당하는 board 인스턴스 얻기
        board_id = request.POST.get('board')
        board = Board.objects.get(id=board_id)
        # 3. Board 와 외래키 관계인 Study 인스턴스 얻기
        study_id = board.study.id
        study = Study.objects.get(id=study_id)
        # 4. Study 의 members 인스턴스 리스트 얻기
        members = study.members.all()

        # members list 값 : [<NanumUser: username1>, <NanumUser: username2>]
        # NanumUser 에서 User id 얻기 : members[1].user.id

        for m in members:
            # VerificationFile 인스턴스 생성 시 인자로 id 대신, 인스턴스 자체를 넘겨준다.
            VerificationFile.objects.create(user=m, verification=verification)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # override : Verification 인스턴스 수정 시, 수정 전용 시리얼라이저를 받아서 진행
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self._get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


@permission_classes((AllowAny,))
class VerificationFileViewSet(viewsets.ModelViewSet):
    queryset = VerificationFile.objects.all()
    serializer_class = VerificationFileGetSerializer

    # override : 생성, 수정 시리얼라이저 반환
    def _get_serializer(self, *args, **kwargs):
        serializer_class = VerificationFileSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # override : VerificationFile 인스턴스 생성 시, 생성 전용 시리얼라이저를 받아서 진행
    def create(self, request, *args, **kwargs):
        serializer = self._get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # override : VerificationFile 인스턴스 수정 시, 수정 전용 시리얼라이저를 받아서 진행
    # 기존 파일 삭제 후, 새로운 파일 생성
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  #
        instance = self.get_object()
        # 실제 파일 삭제
        instance.attached_image.delete()
        serializer = self._get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # override : VerificationFile 인스턴스 삭제 시, 모델 인스턴스, 실제 파일 삭제
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()      # 파일 관련 인스턴스 개체 삭제
        instance.attached_image.delete()  # 실제 파일 삭제
        return super(VerificationFileViewSet, self).destroy(request, *args, **kwargs)
