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


# ===================================================
# ============== type 3 : Verificaiton ==============
# ===================================================
@permission_classes((AllowAny,))
class VerificationViewSet(viewsets.ModelViewSet):
    queryset = Verification.objects.all()
    serializer_class = VerificationGetSerializer

    # override GenericAPIView.get_serializer
    def _get_serializer(self, *args, **kwargs):
        serializer_class = VerificationSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # override ModelViewSet.CreateModelMixin.create
    def create(self, request, *args, **kwargs):
        serializer = self._get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        #
        #
        # Verification.object.create()

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
class VerificationFileViewSet(viewsets.ModelViewSet):
    queryset = VerificationFile.objects.all()
    serializer_class = VerificationFileGetSerializer

    # override GenericAPIView.get_serializer
    def _get_serializer(self, *args, **kwargs):
        serializer_class = VerificationFileSerializer
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
        instance.attached_image.delete()  # 실제 file 삭제
        serializer = self._get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # override
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # override
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()     # file 관련 인스턴스 개체 삭제
        instance.attached_image.delete()  # 실제 file 삭제
        return super(VerificationFileViewSet, self).destroy(request, *args, **kwargs)
