from rest_framework import serializers


from study.models import *
from accounts.models import NanumUser
from accounts.serializer import NanumUserSerializer


class StudySerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = Study
        fields = '__all__'


class MemberSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = Member
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = '__all__'


class NoticeSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = Notice
        fields = '__all__'


class CalenderSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = Calender
        fields = '__all__'


class ReferenceSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = Reference
        fields = '__all__'


class ReferenceCommentSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = ReferenceComment
        fields = '__all__'


class ReferenceFileSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = ReferenceFile
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = Question
        fields = '__all__'


class QuestionCommentSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = QuestionComment
        fields = '__all__'


class QuestionFileSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = QuestionFile
        fields = '__all__'