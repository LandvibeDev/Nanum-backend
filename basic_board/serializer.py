from rest_framework import serializers


from basic_board.models import *
from accounts.models import NanumUser
from accounts.serializer import NanumUserSerializer, UserSerializer
from study.serializer import __dynamic__init__, BoardSerializer


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