from django.db import models
from django.utils import timezone

import os

from abstract.models import AbstractBoard, AbstractComment, AbstractFile
from accounts.models import NanumUser


# 파일 저장 경로 정의
def get_study_thumbnail_path(instance, filename):
    return os.path.join('study', 'thumbnail', 'pk_'+str(instance.id), str(timezone.now()), filename)


class Study(models.Model):
    """
    스터디 관련 정보 클래스
    """
    title = models.CharField(null=False, blank=False, max_length=200, help_text='이름')
    topic = models.CharField(null=False, blank=False, max_length=200, help_text='주제')
    thumbnail = models.ImageField(
        null=True,
        blank=True,
        upload_to=get_study_thumbnail_path,
        help_text='썸네일 이미지'
    )
    start_date = models.DateTimeField(null=True, blank=True, help_text='시작일')
    end_date = models.DateTimeField(null=True, blank=True, help_text='종료일')
    joined_user_count = models.IntegerField(default=0, help_text='스터디 인원')
    max_user_count = models.IntegerField(default=10, help_text='최대 스터디 인원')
    like_count = models.IntegerField(default=0, help_text='좋아요 수')
    is_active = models.BooleanField(default=True, help_text='스터디 진행여부(진행중/끝)')
    is_enrolling = models.BooleanField(default=True, help_text='스터디 모집중(참여가능/불가)')
    likes = models.ManyToManyField(
        NanumUser,
        blank=True,
        related_name='likes',
        through='StudyLike', # Study, NanumUser 의 중계 모델 Like
    )
    members = models.ManyToManyField(
        NanumUser,
        blank=True,
        related_name='members',
        through='StudyMember',  # Study, NanumUser 의 중계 모델 Member
    )

    class Meta:
        ordering = ('-pk', '-start_date', )

    def __str__(self):
        return 'study_' + str(self.id)


class StudyMember(models.Model):
    """
    스터디 멤버 정보 클래스
    """
    study = models.ForeignKey(Study, null=True, blank=True, on_delete=models.CASCADE, help_text='스터디 정보')
    user = models.ForeignKey(NanumUser, null=True, blank=True, on_delete=models.CASCADE, help_text='스터디에 참가한 사용자')
    # position = models.IntegerField(default=1, help_text='스터디 권한, 숫자가 낮을수록 높은권한?')
    joined_date = models.DateTimeField(auto_now_add=True, help_text='스터디 참가일')

    class Meta:
        ordering = ('-pk', '-joined_date', )

    def __str__(self):
        return 'member_' + str(self.id)


class StudyLike(models.Model):
    """
    스터디 선호도/좋아요/추천 정보 클래스
    """
    study = models.ForeignKey(Study, null=True, blank=True, on_delete=models.CASCADE, help_text='스터디 정보')
    user = models.ForeignKey(NanumUser, null=True, blank=True, on_delete=models.CASCADE, help_text='좋아요를 생성한 사용자')
    create_date = models.DateTimeField(auto_now_add=True, help_text='좋아요 누른 날짜')

    class Meta:
        ordering = ('-pk', '-create_date', )

    def __str__(self):
        return 'like_' + str(self.id)


class Board(models.Model):
    """
    Study 와 하위 게시판의 중간역할 클래스
    """
    study = models.ForeignKey(Study, null=True, blank=True, on_delete=models.CASCADE, help_text='스터디 정보')
    type = models.IntegerField(default=0, help_text='게시판의 종류 값')
    title = models.CharField(null=False, blank=False, max_length=200, default='이름 없음', help_text='게시판 이름')
    nickname = models.CharField(null=True, blank=True, max_length=200, default='닉네임', help_text='게시판 별명')
    description = models.CharField(null=True, blank=True, max_length=200, default=' ', help_text='간단한 설명')

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return 'Board_' + str(self.id)
