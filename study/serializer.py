from rest_framework import serializers


from study.models import *
from accounts.models import NanumUser
from accounts.serializer import NanumUserSerializer


class MemberSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = Member
        fields = ('study', 'user', 'joined_date')


class LikeSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ('study', 'user', 'create_date')


class NoticeSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = Notice
        fields = ('title', 'contents', 'count', 'comment_count', 'create_date', 'update_date',
                  'user', 'study')

# 카테고리 정보에서 캘린더 정보 참고
class CalenderInTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = CalenderTag
        exclude = ('calender',)

# 캘린더 정보에서 카테고리 정보 참고
class TagInCalenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calender
        fields = ('id', 'title', 'start_date', 'end_date', 'description', 'study', 'is_oneday', 'is_part_time')


class CalenderSerializer(serializers.ModelSerializer):
    # Calender 에서 Calender Tag 의 정보를 얻는 법
    # models.CalenderTag 에서 정의된 many to many field 에서 related_name을 밑의 Meta class field 에 추가하면 된다.
    # related_name arg 의 default 는 '클래스명(소문자)_set'
    calendertag_set = CalenderInTagSerializer(many=True, read_only=True)
    class Meta:
        model = Calender
        fields = ('id', 'title', 'start_date', 'end_date', 'description', 'study', 'is_oneday', 'is_part_time'
                  , 'calendertag_set')


class CalenderTagSerializer(serializers.ModelSerializer):
    # calender tag 정보 조회 시 연관된 calender 정보를 json 형식으로 불러옴
    calender = TagInCalenderSerializer(many=True, read_only=True)

    class Meta:
        model = CalenderTag
        fields = ('id', 'name', 'calender')


class ReferenceSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = Reference
        fields = ('title', 'contents', 'count', 'comment_count', 'create_date', 'update_date',
                  'user', 'study', 'calender')


class ReferenceCommentSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = ReferenceComment
        fields = ('contents', 'create_date', 'update_date',
                  'user', 'reference')


class ReferenceFileSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = ReferenceFile
        fields = ('name', 'size', 'download_count', 'create_date', 'update_date',
                  'attached_file', 'reference')


class QuestionSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ('title', 'contents', 'count', 'comment_count', 'create_date', 'update_date',
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


class StudySerializer(serializers.ModelSerializer):
    # 여기서 멤버 시리얼라이저를 통해서 멤버 필드를 선언하면 스터디 정보 출력시 해당 모델에 대한 자세한 정보를 알 수 이싿
    # issue 밑에서 정의된 클래스를 위에서 쓸때 어떻게 해야하는가? 그냥 내려
    #members = MemberSerializer(read_only=True, many=True)
    #likes = serializers.RelatedField(read_only=True, many=True)
    #likes = LikeSerializer(many=True, read_only=True)
    class Meta:
        model = Study
        fields = ('pk', 'title', 'topic', 'thumbnail', 'start_date', 'end_date', 'joined_user_count', 'max_user_count', 'is_active', 'is_enrolling', 'likes', 'like_count', 'members', 'likes')
