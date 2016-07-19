from django.db import models
from django.conf import settings
from django.utils import timezone

import os

from abstract.models import AbstractBoard,AbstractComment,AbstractFile
from accounts.models import NanumUser


# 파일 저장 경로 정의
def get_issue_thumbnail_path(instance, filename):
    return os.path.join('issue', 'thumbnail', 'pk_'+str(instance.id), str(timezone.now()), filename)


def get_issue_file_path(instance, filename):
    return os.path.join('issue', 'file', 'pk_'+str(instance.id), str(timezone.now()), filename)


class Issue(AbstractBoard):
    '''
    title = models.CharField(max_length=200, help_text='제목')
    contents = models.TextField(null=True, blank=True, help_text='내용')
    count = models.IntegerField(default=0, help_text='조회수')
    comment_count = models.IntegerField(default=0, help_text='댓글 수')
    create_date = models.DateTimeField(auto_now_add=True, help_text='작성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')
    '''
    like_count = models.IntegerField(default=0, help_text='좋아요 개수')
    thumbnail = models.ImageField(
        blank=True,
        null=True,
        upload_to=get_issue_thumbnail_path,
        help_text='프로필 사진'
    )
    user = models.ForeignKey(NanumUser, null=True, related_name='issue_users')
    likes = models.ManyToManyField(
        NanumUser,
        through='IssueLike',
        through_fields=('issue', 'user'),
        related_name='issue_likes',
        help_text='좋아요'
    )
    tags = models.ManyToManyField(
        'IssueTag',
        blank=True,
        help_text='해시 태그'
    )

    class Meta:
        db_table = 'issue'
        ordering = ('-pk', )

    def __str__(self):
        return 'issue ' + str(self.id)

    # 서버에 저장된 이미지 파일들까지 삭제
    def delete(self, *args, **kwargs):
        self.thumbnail.delete()
        super(Issue, self).delete(*args, **kwargs)


class IssueComment(AbstractComment):
    '''
    contents = models.TextField(help_text='내용')
    create_date = models.DateTimeField(auto_now_add=True, help_text='작성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')
    '''
    user = models.ForeignKey(NanumUser, null=True, related_name='issue_comment_users', help_text='작성자')
    issue = models.ForeignKey(Issue, null=True)

    class Meta:
        db_table = 'issue_comment'
        ordering = ('-pk',)

    def __str__(self):
        return 'issue_comment ' + str(self.id)


class IssueFile(AbstractFile):
    '''
    name = models.CharField(max_length=200, help_text='파일 이름')
    size = models.CharField(max_length=200, help_text="파일 크기(kb) in char type")
    download_count = models.IntegerField(default=0, help_text='다운로드 횟수')
    create_date = models.DateTimeField(auto_now_add=True, help_text='생성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')
    '''
    attached_file = models.FileField(
        null=True,
        upload_to=get_issue_file_path,
        help_text='첨부 파일'
    )
    issue = models.ForeignKey(Issue, null=True)

    class Meta:
        db_table = 'issue_file'
        ordering = ('-pk',)

    def __str__(self):
        return 'issue_file ' + str(self.id)

    # 서버에 저장된 이미지 파일들까지 삭제
    def delete(self, *args, **kwargs):
        self.attached_file.delete()
        super(IssueFile, self).delete(*args, **kwargs)


class IssueTag(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text='해시 태그 이름')

    class Meta:
        db_table = 'issue_tag'
        ordering = ('-pk',)

    def __str__(self):
        return 'issue_tag ' + str(self.id)


class IssueLike(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    user = models.ForeignKey(NanumUser, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True, help_text='좋아요 클릭 시간')

    class Meta:
        db_table = 'issue_like'
        ordering = ('-pk',)

    def __str__(self):
        return 'issue_like ' + str(self.id)
