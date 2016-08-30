from django.db import models
from django.utils import timezone

import os

from abstract.models import AbstractBoard, AbstractComment, AbstractFile
from accounts.models import NanumUser
from study.models import Board


def get_basic_board_file_path(instance, filename):
    return os.path.join('basic_board', 'file', 'pk_'+str(instance.id), str(timezone.now()), filename)


class BasicBoard(AbstractBoard):
    """
    기본적인 기능(공지사항, 자유게시판,) 게시판 클래스

    title = models.CharField(max_length=200, help_text='제목')
    contents = models.TextField(null=True, blank=True, help_text='내용')
    count = models.IntegerField(default=0, help_text='조회수')
    comment_count = models.IntegerField(default=0, help_text='댓글 수')
    create_date = models.DateTimeField(auto_now_add=True, help_text='작성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')
    """
    user = models.ForeignKey(NanumUser, null=True, blank=True, on_delete=models.CASCADE, help_text='게시글을 생성한 사용자')
    board = models.ForeignKey(Board, null=True, blank=True, on_delete=models.CASCADE, help_text='게시판 정보')
    like_count = models.IntegerField(default=0, help_text='게시글에 대한 좋아요 수')
    likes = models.ManyToManyField(
        NanumUser,
        blank=True,
        related_name='basic_board_likes',
        through='BasicBoardLike',  # BasicBoard, NanumUser 의 중계 모델 Like
    )

    class Meta:
        ordering = ('-pk', '-create_date', )

    def __str__(self):
        return 'basic_board_' + str(self.id)


class BasicBoardComment(AbstractComment):
    """
    기본 게시판의 댓글 정보 클래스

    contents = models.TextField(help_text='내용')
    create_date = models.DateTimeField(auto_now_add=True, help_text='작성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')
    """
    user = models.ForeignKey(NanumUser, null=True, blank=True, on_delete=models.CASCADE, help_text='게시글을 생성한 사용자')
    basic_board = models.ForeignKey(BasicBoard, null=True, blank=True, on_delete=models.CASCADE, help_text='게시글')

    class Meta:
        ordering = ('create_date', )

    def __str__(self):
        return 'basic_board_comment_' + str(self.id)


class BasicBoardFile(AbstractFile):
    """
    기본 기능게시글의 첨부파일 클래스

    name = models.CharField(max_length=200, help_text='파일 이름')
    size = models.CharField(max_length=200, help_text="파일 크기(kb) in char type")
    download_count = models.IntegerField(default=0, help_text='다운로드 횟수')
    create_date = models.DateTimeField(auto_now_add=True, help_text='생성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')
    """
    basic_board = models.ForeignKey(BasicBoard, null=True, blank=True, on_delete=models.CASCADE, help_text='게시글')
    attached_file = models.FileField(
        null=True,
        blank=True,
        upload_to=get_basic_board_file_path,
        help_text='게시글 첨부파일'
    )

    class Meta:
        ordering = ('-pk', 'create_date',)

    def __str__(self):
        return 'basic_board_file_' + str(self.id)


class BasicBoardLike(models.Model):
    """
    게시글 선호도/좋아요/추천 정보 클래스
    """
    basic_board = models.ForeignKey(BasicBoard, null=True, blank=True, on_delete=models.CASCADE, help_text='게시글 정보')
    user = models.ForeignKey(NanumUser, null=True, blank=True, on_delete=models.CASCADE, help_text='좋아요 생성 사용자')
    create_date = models.DateTimeField(auto_now_add=True, help_text='좋아요 누른 날짜')

    class Meta:
        ordering = ('-pk', '-create_date', )

    def __str__(self):
        return 'basic_board_like_' + str(self.id)
