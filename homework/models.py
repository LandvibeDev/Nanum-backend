from django.db import models
from django.utils import timezone

import os

from abstract.models import AbstractBoard, AbstractComment, AbstractFile
from accounts.models import NanumUser
from study.models import Study
# Create your models here.


# 파일 저장 경로 정의
def get_homework_file_path(instance, filename):
    return os.path.join('homework', 'homework_file', 'pk_'+str(instance.id), str(timezone.now()), filename)


def get_submit_file_path(instance, filename):
    return os.path.join('homework', 'submit_file', 'pk_'+str(instance.id), str(timezone.now()), filename)


class HomeWork(AbstractBoard):
    """
    과제 정보를 담은 클래스

    title = models.CharField(max_length=200, help_text='제목')
    contents = models.TextField(null=True, blank=True, help_text='내용')
    count = models.IntegerField(default=0, help_text='조회수')
    comment_count = models.IntegerField(default=0, help_text='댓글 수')
    create_date = models.DateTimeField(auto_now_add=True, help_text='작성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')
    """
    end_date = models.DateTimeField(null=False, blank=False, help_text='과제 마감일')
    finished_count = models.DateTimeField(default=0, help_text='과제 제출한 스터디원 수')
    user = models.ForeignKey(NanumUser, null=True, blank=True, on_delete=models.CASCADE, help_text='과제 출제자')
    study = models.ForeignKey(Study, null=True, blank=True, on_delete=models.CASCADE, help_text='과제가 속한 스터디')

    class Meta:
        ordering = ('-pk', '-create_date', )

    def __str__(self):
        return 'homework_' + str(self.id)


# class Comment(AbstractComment):
#     """
#     과제에 대한 댓글 정보를 담은 클래스
#
#     contents = models.TextField(help_text='내용')
#     create_date = models.DateTimeField(auto_now_add=True, help_text='작성일')
#     update_date = models.DateTimeField(auto_now=True, help_text='수정일')
#     """
#     user = models.ForeignKey(NanumUser, null=True, blank=True, on_delete=models.CASCADE, help_text='댓글 작성자')
#     homework = models.ForeignKey(HomeWork, null=True, blank=True, on_delete=models.CASCADE, help_text='과제')
#
#     class Meta:
#         ordering = ('-pk', 'create_date',)
#
#     def __str__(self):
#         return 'comment_' + str(self.id)


class HomeWorkFile(AbstractFile):
    """
    과제 첨부파일 정보를 담은 클래스
    각 인스턴스 = 각 유저가 업로드한 과제

    name = models.CharField(max_length=200, help_text='파일 이름')
    size = models.CharField(max_length=200, help_text="파일 크기(kb) in char type")
    download_count = models.IntegerField(default=0, help_text='다운로드 횟수')
    create_date = models.DateTimeField(auto_now_add=True, help_text='생성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')
    """
    user = models.ForeignKey(NanumUser, null=True, blank=True, on_delete=models.CASCADE, help_text='과제를 제출한 사용자')
    homework = models.ForeignKey(HomeWork, null=True, blank=True, on_delete=models.CASCADE, help_text='첨부파일이 속한 과제')
    attached_file = models.FileField(
        null=True,
        blank=True,
        upload_to=get_homework_file_path,
        help_text='과제 첨부 파일'
    )

    class Meta:
        ordering = ('-pk', 'create_date',)

    def __str__(self):
        return 'attached_file_' + str(self.id)


# class Submit(AbstractComment):
#     """
#     과제 제출에 대한 정보를 담은 클래스
#
#     contents = models.TextField(help_text='내용')
#     create_date = models.DateTimeField(auto_now_add=True, help_text='작성일')
#     update_date = models.DateTimeField(auto_now=True, help_text='수정일')
#     """
#     feedback_count = models.IntegerField(default=0, help_text='피드백 수')
#     user = models.ForeignKey(NanumUser, null=True, blank=True, on_delete=models.CASCADE, help_text='과제 제출자')
#     homework = models.ForeignKey(HomeWork, null=True, blank=True, on_delete=models.CASCADE, help_text='과제')
#     is_finished = models.BooleanField(default=False, help_text='제출 완료 여부')
#
#     class Meta:
#         ordering = ('-pk', 'create_date',)
#
#     def __str__(self):
#         return 'submit_' + str(self.id)


# class SubmitFile(AbstractFile):
#     """
#     제출한 과제의 첨부파일 정보를 담은 클래스
#
#     name = models.CharField(max_length=200, help_text='파일 이름')
#     size = models.CharField(max_length=200, help_text="파일 크기(kb) in char type")
#     download_count = models.IntegerField(default=0, help_text='다운로드 횟수')
#     create_date = models.DateTimeField(auto_now_add=True, help_text='생성일')
#     update_date = models.DateTimeField(auto_now=True, help_text='수정일')
#     """
#     attached_file = models.FileField(
#         null=True,
#         blank=True,
#         upload_to=get_submit_file_path,
#         help_text='첨부 파일'
#     )
#     submit = models.ForeignKey(Submit, null=True, blank=True, on_delete=models.CASCADE, help_text='과제 첨부 파일 댓글')
#
#     class Meta:
#         ordering = ('-pk', 'create_date',)
#
#     def __str__(self):
#         return 'submit_file_' + str(self.id)


# class Feedback(AbstractComment):
#     """
#     제출한 과제에 대한 평가, 피드백 등 정보를 담은 클래스
#
#     contents = models.TextField(help_text='내용')
#     create_date = models.DateTimeField(auto_now_add=True, help_text='작성일')
#     update_date = models.DateTimeField(auto_now=True, help_text='수정일')
#     """
#     user = models.ForeignKey(NanumUser, null=True, blank=True, on_delete=models.CASCADE, help_text='피드백 작성자')
#     submit = models.ForeignKey(Submit, null=True, blank=True, help_text='과제 제출 글')
#
#     class Meta:
#         ordering = ('-pk', 'create_date',)
#
#     def __str__(self):
#         return 'feedback_' + str(self.id)
