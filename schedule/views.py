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

from schedule.models import *
from schedule.serializer import *
from accounts.serializer import *


# ===================================================
# ============== type 4 : Schedule ==============
# ===================================================
@permission_classes((AllowAny,))
class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleGetSerializer

    # GenericAPIView 에 똑같은 이름의 함수가 있다.
    def _get_serializer(self, *args, **kwargs):
        serializer_class = ScheduleSerializer
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
        partial = kwargs.pop('partial', False) #
        instance = self.get_object()
        serializer = self._get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


@permission_classes((AllowAny,))
class ScheduleTagViewSet(viewsets.ModelViewSet):
    queryset = ScheduleTag.objects.all()
    serializer_class = ScheduleTagGetSerializer

    def _get_serializer(self, *args, **kwargs):
        serializer_class = ScheduleTagSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # override ModelViewSet.CreateModelMixin.create
    def create(self, request, *args, **kwargs):
        # 인스턴스 생성 시 사용되는 시리얼라이저를 바꾼다.
        serializer = self._get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # override ModelViewSet.UpdateModelMixin.update
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False) #
        instance = self.get_object()
        serializer = self._get_serializer(instance, data=request.data, partial=partial) #
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
