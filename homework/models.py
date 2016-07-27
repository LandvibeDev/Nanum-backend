from django.db import models

from abstract.models import AbstractBoard, AbstractComment, AbstractFile
from accounts.models import NanumUser
from study.models import Study
# Create your models here.


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
    finished_count = models.DateTimeField(null=False, blank=False, default=0, help_text='과제 제출한 스터디원 수')
    user = models.ForeignKey(NanumUser, null=False, blank=False, on_delete=models.CASCADE, help_text='과제 출제자')
    study = models.ForeignKey(Study, null=False, blank=False, on_delete=models.CASCADE, help_text='과제가 속한 스터디')


class Comment(AbstractComment):
    """
    과제에 대한 댓글 정보를 담은 클래스

    contents = models.TextField(help_text='내용')
    create_date = models.DateTimeField(auto_now_add=True, help_text='작성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')
    """
    user = models.ForeignKey(NanumUser, null=False, blank=False, on_delete=models.CASCADE, help_text='댓글 작성자')
    homework = models.ForeignKey(HomeWork, null=False, blank=False, on_delete=models.CASCADE, help_text='과제')


class AttachedFIle(AbstractFile):
    """
    과제 첨부파일 정보를 담은 클래스

    name = models.CharField(max_length=200, help_text='파일 이름')
    size = models.CharField(max_length=200, help_text="파일 크기(kb) in char type")
    download_count = models.IntegerField(default=0, help_text='다운로드 횟수')
    create_date = models.DateTimeField(auto_now_add=True, help_text='생성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')
    """
    attached_file = models.FileField(null=False, blank=False, help_text='과제 첨부 파일')
    homework = models.ForeignKey(HomeWork, null=False, blank=False, on_delete=models.CASCADE, help_text='첨부파일이 속한 과제')


class Submit(AbstractComment):
    """
    과제 제출에 대한 정보를 담은 클래스

    contents = models.TextField(help_text='내용')
    create_date = models.DateTimeField(auto_now_add=True, help_text='작성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')
    """
    feedback_count = models.IntegerField(null=False, blank=False, default=0, help_text='피드백 수')
    user = models.ForeignKey(NanumUser, null=False, blank=False, on_delete=models.CASCADE, help_text='과제 제출자')
    homework = models.ForeignKey(HomeWork, null=False, blank=False, on_delete=models.CASCADE, help_text='과제')
    is_finished = models.BooleanField(null=False, blank=False, help_text='제출 완료 여부')


class SubmitFile(AbstractFile):
    """
    제출한 과제의 첨부파일 정보를 담은 클래스

    name = models.CharField(max_length=200, help_text='파일 이름')
    size = models.CharField(max_length=200, help_text="파일 크기(kb) in char type")
    download_count = models.IntegerField(default=0, help_text='다운로드 횟수')
    create_date = models.DateTimeField(auto_now_add=True, help_text='생성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')
    """
    attached_file = models.FileField(null=False, blank=False, help_text='첨부 파일')
    submit = models.ForeignKey(Submit, null=False, blank=False, on_delete=models.CASCADE, help_text='과제 첨부 파일 댓글')


class Feedback(AbstractComment):
    """
    제출한 과제에 대한 평가, 피드백 등 정보를 담은 클래스

    contents = models.TextField(help_text='내용')
    create_date = models.DateTimeField(auto_now_add=True, help_text='작성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')
    """
    user = models.ForeignKey(NanumUser, null=False, blank=False, on_delete=models.CASCADE, help_text='피드백 작성자')
    submit = models.ForeignKey(Submit, null=False, blank=False, help_text='과제 제출 글')
