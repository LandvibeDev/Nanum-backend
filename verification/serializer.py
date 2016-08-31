from rest_framework import serializers

from verification.models import *
from accounts.models import NanumUser
from accounts.serializer import NanumUserSerializer, UserSerializer
# from study.serializer import BoardSerializer
from abstract.serializer import __dynamic__init__


class VerificationSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

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


class VerificationGetSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    user = NanumUserSerializer(read_only=True, fields=('user',))
    # board = BoardSerializer(read_only=True, fields=('id', 'study', 'type', 'title'))
    verificationfile_set = VerificationFileSerializer(read_only=True, many=True)

    class Meta:
        model = Verification
        fields = ('id', 'description', 'start_date', 'end_date',
                  'user', 'board',
                  'verificationfile_set')


class VerificationFileGetSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        __dynamic__init__(self, *args, **kwargs)

    user = NanumUserSerializer(read_only=True)
    # verification = VerificationSerializer(read_only=True)

    class Meta:
        model = VerificationFile
        fields = ('id', 'attached_image', 'is_checked', 'upload_date', 'checked_date', 'rank',
                  'user', 'verification')
