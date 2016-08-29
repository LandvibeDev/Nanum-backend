from django.db import models
from django.utils import timezone

import os

from abstract.models import AbstractBoard, AbstractComment, AbstractFile
from accounts.models import NanumUser
from study.models import Board, Study


class Schedule(models.Model):
    """
    스터디 시작/종료날짜, 스터디 관련 일정 정보 클래스
    """
    user = models.ForeignKey(NanumUser, null=True, blank=True, on_delete=models.CASCADE, help_text='일정을 생성한 사용자')
    board = models.ForeignKey(Board, null=True, blank=True, on_delete=models.CASCADE, help_text='일정과 관련된 게시판')
    title = models.CharField(null=False, blank=False, default='제목없는 일정', max_length=200, help_text='일정 제목')
    start_date = models.DateTimeField(null=False, blank=False, auto_now_add=True, help_text='일정 시작일')
    end_date = models.DateTimeField(null=False, blank=False, auto_now_add=True, help_text='일정 종료일')
    description = models.TextField(null=True, blank=True, help_text='일정 설명')
    study = models.ForeignKey(Study, null=True, blank=True, on_delete=models.CASCADE, help_text='스터디')
    is_oneday = models.BooleanField(null=False, blank=False, default=False, help_text='종일 일정 여부')
    color = models.CharField(null=True, blank=True, max_length=200, default='#FFFFFF', help_text='일정 색상')
    linked_type = models.IntegerField(default=-1, help_text='일정과 관련된 글의 종류(과제, 자료 등)')

    class Meta:
        ordering = ('-pk', '-start_date', )

    def __str__(self):
        return 'calendar_' + str(self.id)


class ScheduleTag(models.Model):
    """
    스터디 일정에 대한 카테고리 정보 클래스
    """
    name = models.CharField(null=False, blank=False, max_length=50, help_text='일정 분류')
    # related_name 의 default 값은 '클래스명(소문자)_set', 여기서는 명시적으로 선언함
    schedule = models.ManyToManyField(Schedule, related_name='schedule_tag_set', blank=True, help_text='일정 정보')

    class Meta:
        ordering = ('-pk', 'name',)

    def __str__(self):
        return 'schedule_tag_' + str(self.id)