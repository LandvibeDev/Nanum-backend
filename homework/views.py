from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView

import logging

from homework.models import *
from homework.serializer import *
from accounts.serializer import *
# Create your views here.


class HomeWorkViewSet(viewsets.ModelViewSet):
    queryset = HomeWork.objects.all()
    serializer_class = HomeWorkSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class AttachedFIleViewSet(viewsets.ModelViewSet):
    queryset = AttachedFIle.objects.all()
    serializer_class = AttachedFIleSerializer


class SubmitViewSet(viewsets.ModelViewSet):
    queryset = Submit.objects.all()
    serializer_class = SubmitSerializer


class SubmitFileViewSet(viewsets.ModelViewSet):
    queryset = SubmitFile.objects.all()
    serializer_class = SubmitFileSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer