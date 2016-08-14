from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F

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


class StudyViewSet(viewsets.ModelViewSet):
    """
       ModelViewSet - list, create, retrieve, update, destroy 기능을 자동으로 지원
    """
    queryset = Study.objects.all()
    serializer_class = StudySerializer

    # def create(self, request, *args, **kwargs):
    #    return super.create()


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

@permission_classes((AllowAny,))
class CalenderViewSet(viewsets.ModelViewSet):
    queryset = Calender.objects.all()
    serializer_class = CalenderSerializer

@permission_classes((AllowAny,))
class CalenderTagViewSet(viewsets.ModelViewSet):
    queryset = CalenderTag.objects.all()
    serializer_class = CalenderTagSerializer


class ReferenceViewSet(viewsets.ModelViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer


class ReferenceCommentViewSet(viewsets.ModelViewSet):
    queryset = ReferenceComment.objects.all()
    serializer_class = ReferenceCommentSerializer


class ReferenceFileViewSet(viewsets.ModelViewSet):
    queryset = ReferenceFile.objects.all()
    serializer_class = ReferenceFileSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionCommentViewSet(viewsets.ModelViewSet):
    queryset = QuestionComment.objects.all()
    serializer_class = QuestionCommentSerializer


class QuestionFileViewSet(viewsets.ModelViewSet):
    queryset = QuestionFile.objects.all()
    serializer_class = QuestionFileSerializer


"""
    The @api_view decorator for working with function based views.
    The APIView class for working with class-based views.
"""
# 스터디 좋아요 생성
@api_view(['POST'])
@permission_classes((AllowAny,))
def like_create(request, study_pk=None, format=None):
    if request.method == 'POST':
        #logging.warning("request.data : " + str(request.data), )
        #logging.warning("request.data.__getitem__ :" + str(request.POST.__getitem__),)

        # issue?! : 스터디 좋아요는 한명의 사용자에 대해서 하나만 생성 - 프론트에서
        # issue?! : 스터디 '가'에 대해 좋아요를 누른 사용자A가 스터디 '가' 페이지를 띄울때, 좋아요 정보를 GET해서 뿌려줘야 하나?

        # Like instance 생성할 때 인자로 받은 study_pk 값을 request.POST 에 추가
        request.POST.__setitem__('study', study_pk)
        # Study instance를 불러와서 카운트+1
        study = get_object_or_404(Study, pk=study_pk)
        study.like_count = study.like_count+1
        # 변경 내용을 db에 반영
        study.save()
        # logging.warning("study_like : " + str(study.like_count), )
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logging.warning(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer@permission_classes((AllowAny,)).errors, status=status.HTTP_400_BAD_REQUEST)


# 스터디 좋아요 삭제
@api_view(['DELETE'])
@permission_classes((AllowAny,))
def like_delete(request, study_pk=None, like_pk=None, format=None):
    if request.method == 'DELETE':
        # Study instance를 불러와서 카운트-1
        study = get_object_or_404(Study, pk=study_pk)
        #logging.warning("study.data : " + str(study.__str__), )
        study.like_count = study.like_count-1
        # 변경 내용을 db에 반영
        study.save()

        # 해당 like 인스턴스 삭제
        like = get_object_or_404(Like, pk=like_pk)
        #logging.warning("like.data : " + str(like.__str__), )
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 최근 게시물 조회
# 나중에
@api_view(['GET'])
def lastest(request, study_pk=None):
    pass