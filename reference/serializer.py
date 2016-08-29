from rest_framework import serializers

from study.models import *
from accounts.models import NanumUser
from accounts.serializer import NanumUserSerializer, UserSerializer
from study.serializer import __dynamic__init__, BoardSerializer
from reference.models import Reference, ReferenceFile


# user, study, calendar 의 상세정보를 불러오므로 보안을 위해 read_only arg 추가
# ref 인스턴스 생성 시 아래 시리얼라이저를 이용하면 user, study, calendar id값이 반영안됨
class ReferenceGetSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    # 나눔 유저랑 외래키 관계여서 user안에 user또있음
    user = NanumUserSerializer(read_only=True)
    board = BoardSerializer(read_only=True, fields=('id', 'study', 'type', 'title'))

    class Meta:
        model = Reference
        fields = ('id', 'title', 'contents', 'count', 'comment_count', 'create_date', 'update_date',
                  'user', 'board')


# create, update purpose serializer
class ReferenceSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    class Meta:
        model = Reference
        fields = ('id', 'title', 'contents', 'count', 'comment_count', 'create_date', 'update_date',
                  'user', 'board')


class ReferenceFileSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    class Meta:
        model = ReferenceFile
        fields = ('id', 'name', 'size', 'download_count', 'create_date', 'update_date',
                  'attached_file', 'reference')


class ReferenceFileGetSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    class Meta:
        model = ReferenceFile
        fields = ('id', 'name', 'size', 'download_count', 'create_date', 'update_date',
                  'attached_file', 'reference')
