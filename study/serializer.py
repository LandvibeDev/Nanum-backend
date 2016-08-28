from rest_framework import serializers


from study.models import *
from accounts.models import NanumUser
from accounts.serializer import NanumUserSerializer, UserSerializer


def __dynamic__init__(self, *args, **kwargs):
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

    study = StudySerializer(read_only=True, fields=('id', 'title', 'topic'))

    class Meta:
        model = Board
        fields = ('id', 'type', 'title', 'nickname', 'description',
                  'study')


class BasicBoardSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    class Meta:
        model = BasicBoard
        fields = ('id', 'title', 'contents', 'count', 'comment_count', 'create_date', 'update_date', 'like_count',
                  'user', 'board')


class BasicBoardGetSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    user = NanumUserSerializer(read_only=True)
    board = BoardSerializer(read_only=True)

    class Meta:
        model = BasicBoard
        fields = ('id', 'title', 'contents', 'count', 'comment_count', 'create_date', 'update_date', 'like_count',
                  'user', 'board')


class BasicBoardCommentSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    class Meta:
        model = BasicBoardComment
        fields = ('id', 'contents', 'create_date', 'update_date',
                  'user', 'basic_board')


class BasicBoardGetCommentGetSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    basic_board = BasicBoardSerializer(read_only=True)

    class Meta:
        model = BasicBoardComment
        fields = ('id', 'contents', 'create_date', 'update_date',
                  'user', 'basic_board')


class BasicBoardFileSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    class Meta:
        model = BasicBoardFile
        fields = ('id', 'name', 'size', 'download_count', 'create_date', 'update_date',
                  'basic_board', 'attached_file')


class BasicBoardFileGetSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    basic_board = BasicBoardSerializer(read_only=True)

    class Meta:
        model = BasicBoardFile
        fields = ('id', 'name', 'size', 'download_count', 'create_date', 'update_date',
                  'basic_board', 'attached_file')


class CalendarSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    class Meta:
        model = Calendar
        fields = ('title', 'start_date', 'end_date', 'description', 'study', 'is_oneday', 'color', 'linked_type',
                  'calendar_tag_set', 'user', 'board')


class CalendarTagSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    class Meta:
        model = CalendarTag
        fields = ('name', 'calendar')


class CalendarTagGetSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    # calendar tag 정보 조회 시 연관된 calendar 정보를 json 형식으로 불러옴
    calendar = CalendarSerializer(many=True, read_only=True)

    class Meta:
        model = CalendarTag
        fields = ('id', 'name', 'calendar')


class CalendarGetSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)
    # calendar 에서 calendar Tag 의 정보를 얻는 법
    # models.CalendarTag 에서 정의된 many to many field 에서 related_name을 밑의 Meta class field 에 추가하면 된다.
    # related_name arg 의 default 는 '클래스명(소문자)_set'
    calendar_tag_set = CalendarTagSerializer(many=True, read_only=True, fields=('id', 'name'))
    study = StudySerializer(read_only=True, fields=('id', 'title',))
    class Meta:
        model = Calendar
        fields = ('id', 'title', 'start_date', 'end_date', 'description', 'study', 'is_oneday', 'color', 'linked_type'
                  , 'calendar_tag_set', 'user', 'board')


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

    class Meta:
        model = Study
        fields = ('id', 'title', 'topic', 'thumbnail', 'start_date', 'end_date', 'joined_user_count', 'max_user_count', 'is_active', 'is_enrolling', 'like_count',
                  'likes', 'members',)


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


class VerificationSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    class Meta:
        model = Verification
        fields = ('id', 'description', 'start_date', 'end_date',
                  'user', 'board',)


class VerificationGetSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    user = NanumUserSerializer(read_only=True, fields=('id', 'user'))
    board = BoardSerializer(read_only=True, fields=('id', 'study', 'type', 'title'))

    class Meta:
        model = Verification
        fields = ('id', 'description', 'start_date', 'end_date',
                  'user', 'board',)


class VerificationFileSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    class Meta:
        model = VerificationFile
        fields = ('id', 'attached_image', 'is_checked', 'upload_date', 'checked_date', 'rank',
                  'user', 'verification')


class VerificationFileGetSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    user = NanumUserSerializer(read_only=True)
    verification = VerificationSerializer(read_only=True)

    class Meta:
        model = VerificationFile
        fields = ('id', 'attached_image', 'is_checked', 'upload_date', 'checked_date', 'rank',
                  'user', 'verification')
