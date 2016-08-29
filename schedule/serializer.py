from rest_framework import serializers

from schedule.models import *
from accounts.models import NanumUser
from accounts.serializer import NanumUserSerializer, UserSerializer
from study.serializer import __dynamic__init__, StudySerializer


class ScheduleSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    class Meta:
        model = Schedule
        fields = ('title', 'start_date', 'end_date', 'description', 'study', 'is_oneday', 'color', 'linked_type',
                  'schedule_tag_set', 'user', 'board')


class ScheduleTagSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    class Meta:
        model = ScheduleTag
        fields = ('name', 'schedule')


class ScheduleTagGetSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    # calendar tag 정보 조회 시 연관된 calendar 정보를 json 형식으로 불러옴
    schedule = ScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = ScheduleTag
        fields = ('id', 'name', 'schedule')


class ScheduleGetSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)
    # calendar 에서 calendar Tag 의 정보를 얻는 법
    # models.CalendarTag 에서 정의된 many to many field 에서 related_name을 밑의 Meta class field 에 추가하면 된다.
    # related_name arg 의 default 는 '클래스명(소문자)_set'
    schedule_tag_set = ScheduleTagSerializer(many=True, read_only=True, fields=('id', 'name'))
    study = StudySerializer(read_only=True, fields=('id', 'title',))
    class Meta:
        model = Schedule
        fields = ('id', 'title', 'start_date', 'end_date', 'description', 'study', 'is_oneday', 'color', 'linked_type'
                  , 'schedule_tag_set', 'user', 'board')
