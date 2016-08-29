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

from reference.models import *
from reference.serializer import *
from accounts.serializer import *


# ===================================================
# ============== type 1 : Reference ==============
# ===================================================
@permission_classes((AllowAny,))
class ReferenceViewSet(viewsets.ModelViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceGetSerializer

    """
    get_serializer 함수만 오버라이딩 할 경우 GET할때도 create전용 serializer가 반영되서
    연관된 달력의 세부정보, 사용자, 스터디 정보에 대한 세부정보를 알 수 없다.
    따라서 create, get_serializer 함수를 같이 오버라이딩 해줘야 한다.
    """
    def _get_serializer(self, *args, **kwargs):
        # serializer_class = self.get_serializer_class()
        serializer_class = ReferenceSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # override ModelViewSet.CreateModelMixin.create
    def create(self, request, *args, **kwargs):
        # warning("Reference create : " + str(request.data))
        # warning("ReferenceSerializer : " + str(self.serializer_class.Meta.fields))
        serializer = self._get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # warning("serializer ReferenceCreateSerializercreate : " + str(serializer.validated_data))
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # return super(ReferenceViewSet, self).create(request, *args, **kwargs)

    # override ModelViewSet.UpdateModelMixin.update
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self._get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


@permission_classes((AllowAny,))
class ReferenceFileViewSet(viewsets.ModelViewSet):
    queryset = ReferenceFile.objects.all()
    serializer_class = ReferenceFileGetSerializer

    def _get_serializer(self, *args, **kwargs):
        # serializer_class = self.get_serializer_class()
        serializer_class = ReferenceFileSerializer
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

    # override ModelViewSet.UpdateModelMixin.update
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
        instance = self.get_object()    # file 관련 객체 삭제(super에서)
        instance.attached_file.delete() # 실제 file 삭제
        return super(ReferenceFileViewSet, self).destroy(request, *args, **kwargs)

    # issue?! : 오버라이딩은 어떻게 하는게 효율적이고 가독성 좋은 코드가 나올까?
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #
    # def perform_destroy(self, instance):
    #     instance.attached_file.delete() # file 삭제 코드
    #     instance.delete()
