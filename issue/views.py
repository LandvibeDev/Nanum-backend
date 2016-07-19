from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView

import logging

from issue.models import *
from issue.serializer import IssueCommentSerializer, IssueSerializer, IssueFileSerializer, IssueTagSerializer, IssueLikeSerializer
from accounts.serializer import *
# Create your views here.


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all().prefetch_related('tags', 'likes')
    serializer_class = IssueSerializer

    # def list(self, request):
    #     queryset = Issue.objects.all().prefetch_related('tags')
    #     serializer = IssueSerializer(queryset, many=True)
    #     return Response(serializer.data)

    def create(self, request):
        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, format=None):
        try:
            # 조회수 1증가
            Issue.objects.filter(pk=pk).update(count=F('count')+1)
        except Issue.DoesNotExist:
            return Http404
        # tags, likes 조인 쿼리 최적화 필요
        issue_join = get_object_or_404(self.queryset, pk=pk)
        serializer = IssueSerializer(issue_join)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = IssueComment.objects.all().select_related('user', 'issue')
    serializer_class = IssueCommentSerializer

    def list(self, request, issue_pk=None, format=None):
        try:
            comments = self.queryset.filter(issue_id=issue_pk)
        except comments.DoesNotExist:
            return Http404
        comment_serializer = IssueCommentSerializer(comments, many=True)
        return Response(comment_serializer.data)


class FileViewSet(viewsets.ModelViewSet):
    queryset = IssueFile.objects.all()
    serializer_class = IssueFileSerializer
    # 파일 저장 안됨 (in 관리자 페이지)....


# 이슈 생성 시도 > 태그 생성 > 이슈 생성, issue_pk 필요없는가?
@api_view(['POST'])
def tag_create(request, issue_pk=None, format=None):
    if request.method == 'POST':
        serializer = IssueTagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 태그 삭제
@api_view(['DELETE'])
def tag_delete(request, issue_pk=None, tag_pk=None, format=None ):
    if request.method == 'DELETE':
        tag = get_object_or_404(IssueTag, id=tag_pk)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 좋아요 조회, 생성
@api_view(['GET', 'POST'])
def like_create(request, issue_pk=None, format=None):
    if request.method == 'POST':
        serializer = IssueLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        likes = get_object_or_404(IssueLike, issue=issue_pk)
        # likes = IssueLike.objects.filter(issue=issue_pk)
        serializer = IssueLikeSerializer(likes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 좋아요 삭제
@api_view(['DELETE'])
def like_delete(request, issue_pk=None, like_id=None, format=None):
    if request.method == 'DELETE':
        like = get_object_or_404(IssueLike, issue=issue_pk)
        # like = IssueLike.objects.get(id=like_id)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# JSONResonse 정의
# class JSONResponse(HttpResponse):
#     """
#     An HttpResponse that renders its content into JSON.
#     """
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)

# 각종 메소드들 예시
# class IssueList(APIView):
#     """
#     List all issue, or create a new issue
#     """
#
#     def get(self, request, format=None):
#         issue = Issue.objects.all()
#         serializer = IssueSerializer(issue, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = IssueSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class IssueDetail(APIView):
#     """
#     Retrieve, update or delete a code issue.
#     """
#     def get_object(self, issue_id):
#         try:
#             return Issue.objects.get(pk=issue_id)
#         except Issue.DoesNotExist:
#             return Http404
#
#     def get(self, request, issue_id, format=None):
#         issue = self.get_object(issue_id)
#         serializer = IssueSerializer(issue)
#         return Response(serializer.data)
#
#     def put(self, request, issue_id, format=None):
#         issue = self.get_object(issue_id)
#         serializer = IssueSerializer(issue, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, issue_id, format=None):
#         issue = self.get_object(issue_id)
#         issue.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
