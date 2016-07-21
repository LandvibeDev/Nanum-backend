from django.db import models
from django.contrib.auth.models import User

from abstract.models import AbstractBoard, AbstractComment, AbstractFile



class Study(models.Model):
    """
    스터디 관련 정보를 담은 클래스
    """
    title = models.CharField(null=False, blank=False, max_length=200, help_text='스터디 이름')
    topic = models.CharField(null=False, blank=False, max_length=200, help_text='주제')
    thumbnail = models.ImageField(help_text='스터디 이미지')
    start_date = models.DateTimeField(help_text='스터디 시작')
    end_date = models.DateTimeField(help_text='스터디 끝')
    joined_user_count = models.IntegerField(default=0, help_text='스터디 인원')
    max_user_count = models.IntegerField(default=0, help_text='최대 스터디 인원')
    like_count = models.IntegerField(default=0, help_text='스터디 좋아요')
    is_active = models.BooleanField(help_text='스터디 진행여부(진행중/끝)')
    is_enrolling = models.BooleanField(help_text='스터디 참여가능여부(참여가능/불가)')


class StudyMember(models.Model):
    """
    스터디 멤버 정보를 담은 클래스
    """
    study = models.ForeignKey('Study', null=False, blank=False, on_delete=models.CASCADE, help_text='스터디 정보')
    user = models.ForeignKey('User', null=False, blank=False, on_delete=models.CASCADE, help_text='스터디에 참가한 사용자')
    position = models.IntegerField(default=1, help_text='스터디 권한, 숫자가 낮을수록 높은권한?')
    joined_data = models.DateTimeField(auto_now_add='True', help_text='스터디 참가일')


class StudyLike(models.Model):
    """
    스터디 선호도/좋아요/추천 정보를 담은 클래스
    """
    study = models.ForeignKey('Study', null=False, on_delete=models.CASCADE, help_text='스터디 정보')
    user = models.ForeignKey('User', null=False, on_delete=models.CASCADE, help_text='좋아요를 생성한 사용자')
    create_data = models.DateTimeField(auto_now_add='True', help_text='좋아요 누른 날짜')


class StudyNotice(AbstractBoard):
    """
    스터디 공지사항 정보를 담은 클래스
    """
    user = models.ForeignKey('User', null=False, on_delete=models.CASCADE, help_text='공지사항을 생성한 사용자')
    study = models.ForeignKey('Study', null=False, on_delete=models.CASCADE, help_text='스터디 정보')


class Calender(models.Model):
    """
    스터디 시작/종료날짜, 스터디 관련 일정 정보를 담은 클래스
    """
    start_date = models.DateTimeField(null=False, blank=False, help_text='일정 시작 날짜')
    end_date = models.DateTimeField(null=False, blank=False, help_text='일정 종료 날짜')
    description = models.TextField(null=False, blank=True, default=' ', help_text='일정에 대한 설명')
    study = models.Foreignkey('Study', null=False, on_delete=models.CASCADE, help_text='스터디 정보')
    is_oneday = models.BooleanField(null=False, blank=False, help_text='종일 일정 여부')
    is_part_time = models.BooleanField(null=False, blank=False, help_text='부분 일정 여부')


class CalenderCategory(models.Model):
    """
    스터디 일정에 대한 카테고리 정보를 담은 클래스
    """
    name = models.CharField(null=False, blank=False, help_text='일정 분류')
    calender = models.ForeignKey(null=False, blank=False, on_delete=models.CASCADE, help_text='일정 정보')


class HomeWork(AbstractBoard):
    """
    과제 정보를 담은 클래스
    """
    end_date = models.DateTimeField(null=False, blank=False, help_text='과제 제출 기한')
    finished_count = models.DateTimeField(null=False, blank=False, default=0, help_text='과제 제출한 스터디원 수')
    user = models.ForeignKey('User', null=False, blank=False, on_delete=models.CASCADE, help_text='과제를 생성한 사용자')
    study = models.ForeignKey('Study', null=False, blank=False, on_delete=models.CASCADE, help_text='과제가 속한 스터디')


class HomeWorkFile(AbstractFile):
    """
    과제 첨부파일 정보를 담은 클래스
    """
    attached_file = models.FileField(null=False, blank=False, help_text='과제 첨부 파일')
    homework = models.ForeignKey('HomeWork', null=False, blank=False, on_delete=models.CASCADE, help_text='첨부파일이 속한 과제')


class HomeWorkComment(AbstractComment):
    """
    과제에 대한 제출 정보를 담은 클래스
    """
    recomment_count = models.IntegerField(null=False, blank=False, default=0, help_text='대댓글 수')
    user = models.ForeignKey('Homework', null=False, blank=False, on_delete=models.CASCADE, help_text='과제를 제출한 사용자')
    homework = models.ForeignKey('HomeWork', null=False, blank=False, on_delete=models.CASCADE, help_text='댓글이 속한 과제')
    is_finished = models.BooleanField(null=False, blank=False, help_text='과제 제출 여부')

class HomeWorkCommentFile(AbstractFile):
    """
    제출한 과제의 첨부파일 정보를 담은 클래스
    """
    attached_file = models.FileField(null=False, blank=False, help_text='과제 제출 첨부 파일')
    homework_comment = models.ForeignKey('HomeWorkComment', null=False, blank=False, on_delete=models.CASCADE, help_text='과제 첨부 파일 댓글')


class HomeWorkReComment(AbstractComment):
    """
    제출한 과제에 대한 댓글 정보를 담은 클래스
    여기서 댓글은 과제에 대한 평가, 피드백 등 정보를 담는다.
    """
    user = models.ForeignKey('User', null=False, blank=False, on_delete=models.CASCADE, help_text='사용자')
    homework_comment = models.ForeignKey('HomeWorkComment', null=False, blank=False, help_text='과제 제출 첨부 파일에 대한 댓글')


class Reference(AbstractBoard):
    """
    스터디 참고자료에 대한 클래스
    """
    user = models.ForeignKey('User', null=False, blank=False, on_delete=models.CASCADE, help_text='참고자료를 업로드한 사용자')
    study = models.ForeignKey('Study', null=False, blank=False, on_delete=models.CASCADE, help_text='참고자료와 관련된 스터디')
    calender = models.ForeignKey('Calender', null=False, blank=False, on_delete=models.CASCADE, help_text='참고자료와 관련된 일정')


class ReferenceComment(AbstractComment):
    """
    스터디 참고자료에 대한 댓글 정보를 담은 클래스
    """
    user = models.ForeignKey('User', null=False, blank=False, on_delete=models.CASCADE, help_text='참고자료에 대한 댓글')
    reference = models.ForeignKey('Reference', null=False, blank=False, on_delete=models.CASCADE, help_text='참고자료')


class ReferenceFile(AbstractFile):
    """
    스터디 참고자료에서 첨부파일에 대한 정보를 담은 클래스
    """
    attached_file = models.FileField(null=False, blank=False, help_text='첨부한 참고자료')
    reference = models.ForeignKey('Reference', null=False, blank=False, on_delete=models.CASCADE, help_text='참고자료에 대한 정보')


class Question(AbstractBoard):
    """
    스터디에서 질문 정보를 담은 클래스
    """
    user = models.ForeignKey('User', null=False, blank=False, on_delete=models.CASCADE, help_text='질문글을 생성한 사용자')
    study = models.ForeignKey('Study', null=False, blank=False, on_delete=models.CASCADE, help_text='질문글이 포함된 스터디')


class QuestionComment(AbstractComment):
    """
    스터디 질문에 대한 댓글 정보를 담은 클래스
    """
    user = models.ForeignKey('User', null=False, blank=False, on_delete=models.CASCADE, help_text='질문글에 대한 댓글을 생성한 사용자')
    question = models.ForeignKey('Question', null=False, blank=False, on_delete=models.CASCADE, help_text='댓글에 대한 상위 질문')


class QuestionFile(AbstractFile):
    """
    질문글에서 첨부한 파일에 대한 정보를 담은 클래스
    """
    attached_file = models.FileField(null=False, blank=False, help_text='질문글에 대한 첨부파일')
    question = models.ForeignKey('Question', null=False, blank=False, on_delete=models.CASCADE, help_text='첨부파일이 포함된 질문글')