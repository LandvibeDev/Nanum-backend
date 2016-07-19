from django.db import models
from django.conf import settings
import os


def get_file_path(instance,filename):
    return os.path.join('user', instance.user.username, '%Y%m%d_%H%M%S', filename)


class NanumUser(models.Model):
    '''
    User 모델 확장
    username : 학번, Char, 8자 ( view or 프론트 단에서 검증 )
    password : 비밀번호
    email : 이메일
    first_name : 학번 앞 두글자 ( ex : 12121442 > 12 )
    last_name : 이름
    > get_full_name() : 학번+이름

    groups : 그룹, 권한관리
    user_permissions : 사용자 권한

    is_staff
    is_active
    is_superuser
    last_login : 마지막 로그인 날짜
    date_joined : 가입 날짜
    '''
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True)
    birthday = models.DateField(null=True, blank=True, help_text='생일')
    profile_image = models.ImageField(
        null=True,
        blank=True,
        upload_to=get_file_path,
        help_text='프로필 사진'
    )

    class Meta:
        db_table = 'nanum_user'

    def __str__(self):
        return self.user.username
