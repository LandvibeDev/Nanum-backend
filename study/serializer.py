from rest_framework import serializers

from study.models import *
from accounts.models import NanumUser
from accounts.serializer import NanumUserSerializer, UserSerializer

from basic_board.serializer import BasicBoardSerializer
from reference.serializer import ReferenceSerializer
from homework.serializer import HomeWorkSerializer
from verification.serializer import VerificationSerializer
from schedule.serializer import ScheduleSerializer, ScheduleTagSerializer
from abstract.serializer import __dynamic__init__

"""
    ~~~GetSerializer : 해당 모델의 인스턴스 정보를 요청 시 사용
    ~~~Serializer    : 해당 모델의 인스턴스 생성/수정 시 사용
                       다른 시리얼라이저에서 사용 시 정보 요청용으로 사용
"""


class StudySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    class Meta:
        model = Study
        fields = ('id', 'title', 'topic', 'thumbnail', 'start_date', 'end_date', 'joined_user_count', 'max_user_count', 'is_active', 'is_enrolling', 'like_count',
                  'members', 'likes')


class StudyMemberSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    class Meta:
        model = StudyMember
        fields = ('id', 'study', 'user', 'joined_date')


class StudyMemberGetSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    study = StudySerializer(read_only=True, fields=('id', 'title', 'topic',))
    user = NanumUserSerializer(read_only=True)

    class Meta:
        model = StudyMember
        fields = ('id', 'study', 'user', 'joined_date')


class StudyLikeSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    class Meta:
        model = StudyLike
        fields = ('study', 'user', 'create_date')

"""
    TagIncalendarSerializer 클래스 안만들고 CalendarTagSerializer 에서
    calendar = serializer.StringRelatedField(many=True, read_only=True, slug_field='title') 사용. calendar.__str__() 메소드 실행됨
    * slug_filed 는 string 타입만 가능, 튜플 형태로 2개 이상의 필드 동시참조 안됨
    calendar Model에 대한 정보를 참조 가능
    그러나, string 으로 정보가 넘어와서 json으로 파싱하기 번거롭다(해보진 않음)
"""


class BoardSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    class Meta:
        model = Board
        fields = ('id', 'type', 'title', 'nickname', 'description',
                  'study')


class BoardGetSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    study = StudySerializer(read_only=True)
    basicboard_set = BasicBoardSerializer(read_only=True, many=True, fields=('id', 'title','contents'))
    reference_set = ReferenceSerializer(read_only=True, many=True)
    homework_set = HomeWorkSerializer(read_only=True, many=True)
    verification_set = VerificationSerializer(read_only=True, many=True)
    schedule_set = ScheduleSerializer(read_only=True, many=True)

    class Meta:
        model = Board
        fields = ('id', 'type', 'title', 'nickname', 'description',
                  'study',
                  'basicboard_set', 'reference_set', 'homework_set', 'verification_set', 'schedule_set')


# 스터디 정보에서 좋아요에 대한 세부정보 참고
class StudyLikeSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)
    # user = NanumUserSerializer(many=True, read_only=True)
    # user = serializers.SlugRelatedField(read_only=True, many=True, slug_field='user')

    class Meta:
        model = StudyLike
        fields = ('id', 'user', 'create_date',)


class StudyGetSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    # likes = StudyLikeSerializer(many=True, read_only=True, fields=('create_date',))
    # members = StudyMemberSerializer(many=True, read_only=True)
    board_set = BoardSerializer(read_only=True, many=True)

    class Meta:
        model = Study
        fields = ('id', 'title', 'topic', 'thumbnail', 'start_date', 'end_date', 'joined_user_count', 'max_user_count', 'is_active', 'is_enrolling', 'like_count',
                  'likes', 'members', 'board_set')