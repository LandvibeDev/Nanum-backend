from django.db import models

from abstract.models import AbstractBoard, AbstractComment, AbstractFile
from accounts.models import NanumUser



class Study(models.Model):
    """
    스터디 관련 정보를 담은 클래스
    """
    title = models.CharField(null=False, blank=False, max_length=200, help_text='이름')
    topic = models.CharField(null=False, blank=False, max_length=200, help_text='주제')
    thumbnail = models.ImageField(help_text='썸네일 이미지')
    start_date = models.DateTimeField(help_text='시작일')
    end_date = models.DateTimeField(help_text='종료일')
    joined_user_count = models.IntegerField(default=0, help_text='스터디 인원')
    max_user_count = models.IntegerField(default=0, help_text='최대 스터디 인원')
    like_count = models.IntegerField(default=0, help_text='좋아요 수')
    is_active = models.BooleanField(help_text='스터디 진행여부(진행중/끝)')
    is_enrolling = models.BooleanField(help_text='스터디 모집중(참여가능/불가)')


class Member(models.Model):
    """
    스터디 멤버 정보를 담은 클래스
    """
    study = models.ForeignKey(Study, null=False, blank=False, on_delete=models.CASCADE, help_text='스터디 정보')
    user = models.ForeignKey(NanumUser, null=False, blank=False, on_delete=models.CASCADE, help_text='스터디에 참가한 사용자')
    position = models.IntegerField(default=1, help_text='스터디 권한, 숫자가 낮을수록 높은권한?')
    joined_data = models.DateTimeField(auto_now_add='True', help_text='스터디 참가일')


class Like(models.Model):
    """
    스터디 선호도/좋아요/추천 정보를 담은 클래스
    """
    study = models.ForeignKey(Study, null=False, on_delete=models.CASCADE, help_text='스터디 정보')
    user = models.ForeignKey(NanumUser, null=False, on_delete=models.CASCADE, help_text='좋아요를 생성한 사용자')
    create_data = models.DateTimeField(auto_now_add='True', help_text='좋아요 누른 날짜')


class Notice(AbstractBoard):
    """
    스터디 공지사항 정보를 담은 클래스

    title = models.CharField(max_length=200, help_text='제목')
    contents = models.TextField(null=True, blank=True, help_text='내용')
    count = models.IntegerField(default=0, help_text='조회수')
    comment_count = models.IntegerField(default=0, help_text='댓글 수')
    create_date = models.DateTimeField(auto_now_add=True, help_text='작성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')
    """
    user = models.ForeignKey(NanumUser, null=False, on_delete=models.CASCADE, help_text='작성자')
    study = models.ForeignKey(Study, null=False, on_delete=models.CASCADE, help_text='스터디')


class Calender(models.Model):
    """
    스터디 시작/종료날짜, 스터디 관련 일정 정보를 담은 클래스
    """
    start_date = models.DateTimeField(null=False, blank=False, help_text='일정 시작일')
    end_date = models.DateTimeField(null=False, blank=False, help_text='일정 종료일')
    description = models.TextField(null=False, blank=True, default=' ', help_text='일정 설명')
    study = models.ForeignKey(Study, null=False, on_delete=models.CASCADE, help_text='스터디')
    is_oneday = models.BooleanField(null=False, blank=False, help_text='종일 일정 여부')
    is_part_time = models.BooleanField(null=False, blank=False, help_text='부분 일정 여부')


class CalenderCategory(models.Model):
    """
    스터디 일정에 대한 카테고리 정보를 담은 클래스
    """
    name = models.CharField(null=False, blank=False, max_length=30,help_text='일정 분류')
    calender = models.ForeignKey(Calender,null=False, blank=False, on_delete=models.CASCADE, help_text='일정 정보')


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
    user = models.ForeignKey(NanumUser, null=False, blank=False, on_delete=models.CASCADE, help_text='참고자료를 업로드한 사용자')
    study = models.ForeignKey(Study, null=False, blank=False, on_delete=models.CASCADE, help_text='참고자료와 관련된 스터디')
    calender = models.ForeignKey(Calender, null=False, blank=False, on_delete=models.CASCADE, help_text='참고자료와 관련된 일정')


class ReferenceComment(AbstractComment):
    """
    스터디 참고자료에 대한 댓글 정보를 담은 클래스

    contents = models.TextField(help_text='내용')
    create_date = models.DateTimeField(auto_now_add=True, help_text='작성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')
    """
    user = models.ForeignKey(NanumUser, null=False, blank=False, on_delete=models.CASCADE, help_text='참고자료에 대한 댓글')
    reference = models.ForeignKey(Reference, null=False, blank=False, on_delete=models.CASCADE, help_text='참고자료')


class ReferenceFile(AbstractFile):
    """
    스터디 참고자료에서 첨부파일에 대한 정보를 담은 클래스

    name = models.CharField(max_length=200, help_text='파일 이름')
    size = models.CharField(max_length=200, help_text="파일 크기(kb) in char type")
    download_count = models.IntegerField(default=0, help_text='다운로드 횟수')
    create_date = models.DateTimeField(auto_now_add=True, help_text='생성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')
    """
    attached_file = models.FileField(null=False, blank=False, help_text='첨부한 참고자료')
    reference = models.ForeignKey(Reference, null=False, blank=False, on_delete=models.CASCADE, help_text='참고자료에 대한 정보')


class Question(AbstractBoard):
    """
    스터디에서 질문 정보를 담은 클래스

    title = models.CharField(max_length=200, help_text='제목')
    contents = models.TextField(null=True, blank=True, help_text='내용')
    count = models.IntegerField(default=0, help_text='조회수')
    comment_count = models.IntegerField(default=0, help_text='댓글 수')
    create_date = models.DateTimeField(auto_now_add=True, help_text='작성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')
    """
    user = models.ForeignKey(NanumUser, null=False, blank=False, on_delete=models.CASCADE, help_text='질문글을 생성한 사용자')
    study = models.ForeignKey(Study, null=False, blank=False, on_delete=models.CASCADE, help_text='질문글이 포함된 스터디')


class QuestionComment(AbstractComment):
    """
    스터디 질문에 대한 댓글 정보를 담은 클래스

    contents = models.TextField(help_text='내용')
    create_date = models.DateTimeField(auto_now_add=True, help_text='작성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')
    """
    user = models.ForeignKey(NanumUser, null=False, blank=False, on_delete=models.CASCADE, help_text='질문글에 대한 댓글을 생성한 사용자')
    question = models.ForeignKey(Question, null=False, blank=False, on_delete=models.CASCADE, help_text='댓글에 대한 상위 질문')


class QuestionFile(AbstractFile):
    """
    질문글에서 첨부한 파일에 대한 정보를 담은 클래스

    name = models.CharField(max_length=200, help_text='파일 이름')
    size = models.CharField(max_length=200, help_text="파일 크기(kb) in char type")
    download_count = models.IntegerField(default=0, help_text='다운로드 횟수')
    create_date = models.DateTimeField(auto_now_add=True, help_text='생성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')
    """
    attached_file = models.FileField(null=False, blank=False, help_text='질문글에 대한 첨부파일')
    question = models.ForeignKey(Question, null=False, blank=False, on_delete=models.CASCADE, help_text='첨부파일이 포함된 질문글')