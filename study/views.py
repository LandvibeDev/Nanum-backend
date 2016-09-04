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

from study.models import *
from study.serializer import *
from accounts.serializer import *
#from study.models import *

"""
    The @api_view decorator for working with function based views.
    The APIView class for working with class-based views.
"""
"""
    ModelViewSet - list, create, retrieve, update, destroy 기능을 자동으로 지원
"""


@permission_classes((AllowAny,))
class StudyViewSet(viewsets.ModelViewSet):

    queryset = Study.objects.all()
    serializer_class = StudyGetSerializer

    def _get_serializer(self, *args, **kwargs):
        serializer_class = StudySerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # override
    def create(self, request, *args, **kwargs):
        serializer = self._get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # override
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self._get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


@permission_classes((AllowAny,))
class StudyMemberViewSet(viewsets.ModelViewSet):
    queryset = StudyMember.objects.all()
    serializer_class = StudyMemberGetSerializer

    def _get_serializer(self, *args, **kwargs):
        serializer_class = StudyMemberSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # override ModelViewSet.CreateModelMixin.create
    def create(self, request, *args, **kwargs):
        # request POST 요청에 포함된 data얻는 법
        # study 멤버 수 +1
        study_id = request.POST.__getitem__('study')
        study = get_object_or_404(Study, pk=study_id)
        study.joined_user_count += 1
        study.save()

        serializer = self._get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # override ModelViewSet.UpdateModelMixin.update
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self._get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # override
    def destroy(self, request, *args, **kwargs):
        # study 멤버 수 -1
        study_id = request.POST.__getitem__('study')
        study = get_object_or_404(Study, pk=study_id)
        study.joined_user_count -= 1
        study.save()
        return super(StudyMemberViewSet, self).destroy(request, *args, **kwargs)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = StudyLike.objects.all()
    serializer_class = StudyLikeSerializer


# ===================================================
# ============== Board ==============
# ===================================================
@permission_classes((AllowAny,))
class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardGetSerializer

    def _get_serializer(self, *args, **kwargs):
        serializer_class = BoardSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # override ModelViewSet.CreateModelMixin.create
    def create(self, request, *args, **kwargs):
        serializer = self._get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # override Mode lViewSet.UpdateModelMixin.update
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self._get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


# ===================================================
# ============== StudyLike ==============
# ===================================================
# 스터디 좋아요 생성
@api_view(['POST'])
@permission_classes((AllowAny,))
def study_like_create(request, study_pk=None, format=None):
    if request.method == 'POST':
        logging.warning("request.data : " + str(request.data), )
        #logging.warning("request.data.__getitem__ :" + str(request.POST.__getitem__),)

        # issue?! : 스터디 좋아요는 한명의 사용자에 대해서 하나만 생성 - 프론트에서
        # issue?! : 스터디 '가'에 대해 좋아요를 누른 사용자A가 스터디 '가' 페이지를 띄울때, 좋아요 정보를 GET해서 뿌려줘야 하나?

        # Like instance 생성할 때 인자로 받은 study_pk 값을 request.POST 에 추가
        request.POST.__setitem__('study', study_pk)
        """
        request 자체는 immutable 하므로 mutable 한 복제 인스턴스 활용
        request_copy = request.POST.copy()
        rerquest_copy.__setitem__('study', study_pk)
        """
        # study 좋아요  수 증가 및 적용
        study = get_object_or_404(Study, pk=study_pk)
        study.like_count += 1
        study.save()
        # logging.warning("study_like : " + str(study.like_count), )
        serializer = StudyLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # logging.warning(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer@permission_classes((AllowAny,)).errors, status=status.HTTP_400_BAD_REQUEST)


# 스터디 좋아요 삭제
@api_view(['DELETE'])
@permission_classes((AllowAny,))
def study_like_delete(request, study_pk=None, like_pk=None, format=None):
    if request.method == 'DELETE':
        # study 좋아요 수 감소 및 적용
        study = get_object_or_404(Study, pk=study_pk)
        study.like_count -= 1
        study.save()

        # 해당 like 인스턴스 삭제
        like = get_object_or_404(StudyLike, pk=like_pk)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ===================================================
# ============== BasicBoardLike ==============
# ===================================================
# 게시글 좋아요 수 증가
# @api_view(['PUT', 'PATCH'])
# @permission_classes((AllowAny,))
# def basic_board_like_create(request, basic_board_pk=None, format=None):
#     if request.method == 'PUT' or 'PATCH':
#         # Like instance 생성할 때 인자로 받은 basic_board_pk 값을 request.POST 에 추가
#         request.POST.__setitem__('basic_board', basic_board_pk)
#         # study 좋아요  수 증가 및 적용
#         basic_board = get_object_or_404(BasicBoard, pk=basic_board_pk)
#         basic_board.like_count += 1
#         basic_board.save()


# # 게시글 좋아요 수 감소
# @api_view(['PUT'])
# @permission_classes((AllowAny,))
# def basic_board_like_delete(request, basic_board_pk=None, like_pk=None, format=None):
#     if request.method == 'PUT' or 'PATCH':
#         # basic_board 좋아요 수 감소 및 적용
#         basic_board = get_object_or_404(BasicBoard, pk=basic_board_pk)
#         basic_board.like_count -= 1
#         basic_board.save()
#
#         # 해당 basic_board like 인스턴스 삭제
#         like = get_object_or_404(StudyLike, pk=like_pk)
#         like.delete()
#         return Response(status=status.HTTP_20)



# 최근 게시물 조회
# 나중에
# @api_view(['GET'])
# def lastest(request, study_pk=None):
#     pass