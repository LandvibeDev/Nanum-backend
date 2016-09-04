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

from basic_board.models import *
from basic_board.serializer import *
from accounts.serializer import *


# ===================================================
# ============== type 0 : BasicBoard ==============
# ===================================================
@permission_classes((AllowAny,))
class BasicBoardViewSet(viewsets.ModelViewSet):
    queryset = BasicBoard.objects.all()
    # get 시리얼라이저
    serializer_class = BasicBoardGetSerializer

    # override GenericAPIView.get_serializer
    def _get_serializer(self, *args, **kwargs):
        # create, update 시리얼라이저
        serializer_class = BasicBoardSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # override ModelViewSet.CreateModelMixin.create
    def create(self, request, *args, **kwargs):
        serializer = self._get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # override ModelViewSet.UpdateModelMixin.update
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  #
        instance = self.get_object()
        serializer = self._get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


@permission_classes((AllowAny,))
class BasicBoardCommentViewSet(viewsets.ModelViewSet):
    queryset = BasicBoardComment.objects.all()
    serializer_class = BasicBoardGetCommentGetSerializer

    # override GenericAPIView.get_serializer
    def _get_serializer(self, *args, **kwargs):
        serializer_class = BasicBoardCommentSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # override ModelViewSet.CreateModelMixin.create
    def create(self, request, *args, **kwargs):
        serializer = self._get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # override ModelViewSet.UpdateModelMixin.update
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  #
        instance = self.get_object()
        serializer = self._get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


@permission_classes((AllowAny,))
class BasicBoardFileViewSet(viewsets.ModelViewSet):
    queryset = BasicBoardFile.objects.all()
    serializer_class = BasicBoardFileGetSerializer

    def _get_serializer(self, *args, **kwargs):
        # serializer_class = self.get_serializer_class()
        serializer_class = BasicBoardFileSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # override
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # 다운로드 수 증가 및 적용
        instance.download_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # override
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        instance.attached_file.delete()  # 실제 file 삭제
        serializer = self._get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # override
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()     # file 관련 인스턴스 개체 삭제
        instance.attached_file.delete()  # 실제 file 삭제
        return super(BasicBoardFileViewSet, self).destroy(request, *args, **kwargs)

