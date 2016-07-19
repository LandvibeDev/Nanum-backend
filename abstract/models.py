from django.db import models
# Create your models here.


class AbstractBoard(models.Model):
    """
    게시판에 필요한 필드, 함수들 추상화
    상속을 받아 사용
    user, comment, file의 외래키는 상속받은 클래스에서 선언해준다
    """
    title = models.CharField(max_length=200, help_text='제목')
    contents = models.TextField(null=True, blank=True, help_text='내용')
    count = models.IntegerField(default=0, help_text='조회수')
    comment_count = models.IntegerField(default=0, help_text='댓글 수')
    create_date = models.DateTimeField(auto_now_add=True, help_text='작성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')

    class Meta:
        abstract = True

    def __str__(self):
        return 'board' + str(self.id)


class AbstractComment(models.Model):
    """
    게시글 댓글에 필요한 필드, 함수들 추상화
    상속을 받아 사용
    user의 외래키는 상속받은 클래스에서 선언해준다
    """
    contents = models.TextField(help_text='내용')
    create_date = models.DateTimeField(auto_now_add=True, help_text='작성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')

    class Meta:
        abstract = True

    def __str__(self):
        return 'comment' + str(self.id)


class AbstractFile(models.Model):
    """
    게시글의 첨부파일에 필요한 필드, 함수들 추상화
    상속을 받아 사용
    파일 경로는 상속받은 곳에서 직접 선언한다 ( 업로드 경로가 모두 다르기 때문)
    #attached_File = models.FileField(upload_to="{path}")
    """
    name = models.CharField(max_length=200, help_text='파일 이름')
    # unique_name = models.CharField(max_length=200,
    #                                unique=True,
    #                                help_text="prevent to duplicate file name, make of upload_date_time + name")
    size = models.CharField(max_length=200, help_text="파일 크기(kb) in char type")
    download_count = models.IntegerField(default=0, help_text='다운로드 횟수')
    create_date = models.DateTimeField(auto_now_add=True, help_text='생성일')
    update_date = models.DateTimeField(auto_now=True, help_text='수정일')

    class Meta:
        abstract = True

    def __str__(self):
        return 'file' + str(self.id)