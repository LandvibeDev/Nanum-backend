from django.db import models
from django.utils import timezone

import os

from abstract.models import AbstractBoard, AbstractComment, AbstractFile
from accounts.models import NanumUser
from study.models import Board


# 파일 저장 경로 정의
def get_reference_file_path(instance, filename):
    return os.path.join('reference', 'file', 'pk_'+str(instance.id), str(timezone.now()), filename)


class Reference(AbstractBoard):
    """
    스터디 참고자료에 대한 클래스

    title = models.CharField(max_length=200, help_text='제목')
    contents = models.TextField(null=True, blank=True, help_text='내용')
    count = models.IntegerField(default=0, help_text='조회수')
    comment_count = models.IntegerField(default=0, help_text='댓글 수')
    create_date = models.DateTimeField(auto_now_add=True, help_text='작성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')
    """
    user = models.ForeignKey(NanumUser, null=True, blank=True, on_delete=models.CASCADE, help_text='참고자료를 업로드한 사용자')
    board = models.ForeignKey(Board, null=True, blank=True, on_delete=models.CASCADE, help_text='참고자료와 관련된 게시판')

    class Meta:
        ordering = ('-pk', '-create_date', )

    def __str__(self):
        return 'reference_' + str(self.id)


class ReferenceFile(AbstractFile):
    """
    스터디 참고자료에서 첨부파일에 대한 정보 클래스

    name = models.CharField(max_length=200, help_text='파일 이름')
    size = models.CharField(max_length=200, help_text="파일 크기(kb) in char type")
    download_count = models.IntegerField(default=0, help_text='다운로드 횟수')
    create_date = models.DateTimeField(auto_now_add=True, help_text='생성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')
    """
    attached_file = models.FileField(
        null=True,
        blank=True,
        upload_to=get_reference_file_path,
        help_text='첨부한 참고자료'
    )
    reference = models.ForeignKey(Reference, null=True, blank=True, on_delete=models.CASCADE, help_text='참고자료에 대한 정보')

    class Meta:
        ordering = ('-pk', 'create_date', )

    def __str__(self):

        return 'reference_file_' + str(self.id)
