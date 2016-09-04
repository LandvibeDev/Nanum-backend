from django.db import models
from django.utils import timezone

import os

from abstract.models import AbstractBoard, AbstractComment, AbstractFile
from accounts.models import NanumUser
from study.models import Board


def get_verification_file_path(instance, filename):
    return os.path.join('verification', 'file', 'pk_'+str(instance.id), str(timezone.now()), filename)


class Verification(models.Model):
    """
    해당 날짜의 인증내역을 모아놓은 클래스
    """
    user = models.ForeignKey(NanumUser, null=True, blank=True, on_delete=models.CASCADE, help_text='인증 토픽을 생성한 사용자')
    board = models.ForeignKey(Board, null=True, blank=True, on_delete=models.CASCADE, help_text='게시판 정보')
    description = models.CharField(null=True, blank=True, max_length=200, default=' ', help_text='간단한 설명')
    start_date = models.DateTimeField(null=True, blank=True, help_text='시작일')
    end_date = models.DateTimeField(null=True, blank=True, help_text='종료일')

    class Meta:
        ordering = ('-pk', 'start_date',)

    def __str__(self):
        return 'verification_' + str(self.id)


class VerificationFile(models.Model):
    """
    인증 시 사용자가 생성한 파일 클래스
    """
    user = models.ForeignKey(NanumUser, null=True, blank=True, on_delete=models.CASCADE, help_text='인증 완료한 사용자')
    verification = models.ForeignKey(Verification, null=True, blank=True, on_delete=models.CASCADE, help_text='인증 정보')
    attached_image = models.ImageField(
        null=True,
        blank=True,
        upload_to=get_verification_file_path,
        help_text='인증 첨부파일'
    )
    is_checked = models.BooleanField(default=False, help_text='인증여부')
    upload_date = models.DateTimeField(auto_now_add=True, help_text='인증 업로드 날짜')
    checked_date = models.DateTimeField(auto_now=True, help_text='인증 확인 날짜')
    rank = models.IntegerField(default='0', help_text='인증 순위(스터디장이 결정)')

    class Meta:
        ordering = ('-pk', 'upload_date',)

    def __str__(self):
        return 'verification_file_' + str(self.id)

