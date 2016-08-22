from rest_framework import serializers


from study.models import *
from accounts.models import NanumUser
from accounts.serializer import NanumUserSerializer, UserSerializer


def dynamic__init__(self, *args, **kwargs):
    """
    참고 링크 - http://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields

    __init__ 함수를 오버라이딩 하여 다음과 같이 Serializer instance 생성 시 fields tuple을 인자로 넘기도록 함.
    MySerializer(user, fields=('a', 'b', 'c'))
    a, b, c field 정보만 출력가능
    """
    # Don't pass the 'fields' arg up to the superclass
    fields = kwargs.pop('fields', None)

    # Instantiate the superclass normally
    super(serializers.ModelSerializer, self).__init__(*args, **kwargs)

    if fields is not None:
        # Drop any fields that are not specified in the `fields` argument.
        allowed = set(fields)
        existing = set(self.fields.keys())
        for field_name in existing - allowed:
            self.fields.pop(field_name)

class StudyGetSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        dynamic__init__(self, *args, **kwargs)

    class Meta:
        model = Study
        fields = ('id', 'title', 'topic', 'thumbnail', 'start_date', 'end_date', 'joined_user_count', 'max_user_count', 'is_active', 'is_enrolling', 'likes', 'like_count', 'members', 'likes')


class MemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'study', 'user', 'joined_date')


class MemberSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        dynamic__init__(self, *args, **kwargs)

    study = StudyGetSerializer(read_only=True, fields=('id', 'title', 'topic',))
    user = NanumUserSerializer(read_only=True)

    class Meta:
        model = Member
        fields = ('id', 'study', 'user', 'joined_date')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('study', 'user', 'create_date')


class NoticeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ('title', 'contents', 'count', 'comment_count', 'create_date', 'update_date',
                  'user', 'study')

class NoticeSerializer(serializers.ModelSerializer):
    user = NanumUserSerializer(read_only=True)
    study = StudyGetSerializer(read_only=True, fields=('id', 'title',))

    class Meta:
        model = Notice
        fields = ('id', 'title', 'contents', 'count', 'comment_count', 'create_date', 'update_date',
                  'user', 'study')
"""
    TagInCalenderSerializer 클래스 안만들고 CalenderTagSerializer 에서
    calender = serializer.StringRelatedField(many=True, read_only=True, slug_field='title') 사용. Calender.__str__() 메소드 실행됨
    * slug_filed 는 string 타입만 가능, 튜플 형태로 2개 이상의 필드 동시참조 안됨
    Calender Model에 대한 정보를 참조 가능
    그러나, string 으로 정보가 넘어와서 json으로 파싱하기 번거롭다(해보진 않음)
"""
# 다른 모델이 캘린더 정보 참고할 때 쓰는 시리얼라이저
class CalenderGetSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        dynamic__init__(self, *args, **kwargs)

    class Meta:
        model = Calender
        fields = ('id', 'title', 'start_date', 'end_date', 'description', 'study', 'is_oneday', 'is_part_time')

# 캘린더 태크 생성 시리얼라이저
class CalenderTagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalenderTag
        fields = ('name', 'calender')


class CalenderTagSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        dynamic__init__(self, *args, **kwargs)

    # calender tag 정보 조회 시 연관된 calender 정보를 json 형식으로 불러옴
    calender = CalenderGetSerializer(many=True, read_only=True)

    class Meta:
        model = CalenderTag
        fields = ('id', 'name', 'calender')


class CalenderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calender
        fields = ('title', 'start_date', 'end_date', 'description', 'study', 'is_oneday', 'is_part_time'
                  , 'calendertag_set')


class CalenderSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        dynamic__init__(self, *args, **kwargs)
    # Calender 에서 Calender Tag 의 정보를 얻는 법
    # models.CalenderTag 에서 정의된 many to many field 에서 related_name을 밑의 Meta class field 에 추가하면 된다.
    # related_name arg 의 default 는 '클래스명(소문자)_set'
    calendertag_set = CalenderTagSerializer(many=True, read_only=True, fields=('id', 'name'))
    study = StudyGetSerializer(read_only=True, fields=('id', 'title',))
    class Meta:
        model = Calender
        fields = ('id', 'title', 'start_date', 'end_date', 'description', 'study', 'is_oneday', 'is_part_time'
                  , 'calendertag_set')



class QuestionSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'title', 'contents', 'count', 'comment_count', 'create_date', 'update_date',
                  'user', 'study')


class QuestionCommentSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = QuestionComment
        fields = ('contents', 'create_date', 'update_date',
                  'user', 'question')


class QuestionFileSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = QuestionFile
        fields = ('contents', 'create_date', 'update_date',
                  'user', 'question')

# 스터디 정보에서 좋아요에 대한 세부정보 참고
class LikeSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        dynamic__init__(self, *args, **kwargs)
    # user = NanumUserSerializer(many=True, read_only=True)
    # user = serializers.SlugRelatedField(read_only=True, many=True, slug_field='user')

    class Meta:
        model = Like
        fields = ('id', 'user', 'create_date',)

class StudySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        dynamic__init__(self, *args, **kwargs)

    # likes = LikeSerializer(many=True, read_only=True)
    # members = MemberSerializer(many=True, read_only=True)

    class Meta:
        model = Study
        fields = ('id', 'title', 'topic', 'thumbnail', 'start_date', 'end_date', 'joined_user_count', 'max_user_count', 'is_active', 'is_enrolling', 'likes', 'like_count', 'members', 'likes')


# user, study, calender의 상세정보를 불러오므로 보안을 위해 read_only arg 추가
# ref 인스턴스 생성 시 아래 시리얼라이저를 이용하면 user, study, calender id값이 반영안됨
class ReferenceSerializer(serializers.ModelSerializer):
    # 나눔 유저랑 외래키 관계여서 user안에 user또있음
    user = NanumUserSerializer(read_only=True)
    study = StudySerializer(read_only=True, fields=('title', 'topic',))
    calender = CalenderSerializer(read_only=True, fields=('title', 'start_date', 'end_date',))

    class Meta:
        model = Reference
        fields = ('id', 'title', 'contents', 'count', 'comment_count', 'create_date', 'update_date',
                  'user', 'study', 'calender')


# create, update purpose serializer
class ReferenceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ('title', 'contents', 'count', 'comment_count', 'create_date', 'update_date',
                  'user', 'study', 'calender')


# user, reference의 상세 정보가 아니라, id만 불러오므로 위의 ReferenceCreateSerializer 와 같이 따로 안만듬
class ReferenceCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceComment
        fields = ('contents', 'create_date', 'update_date',
                  'user', 'reference')


class ReferenceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceFile
        fields = ('name', 'size', 'download_count', 'create_date', 'update_date',
                  'attached_file', 'reference')