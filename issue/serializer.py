from django.shortcuts import get_object_or_404, render

from rest_framework import serializers

from issue.models import Issue,IssueTag,IssueComment,IssueFile,IssueLike
from accounts.serializer import NanumUserSerializer, UserSerializer
from accounts.models import NanumUser


# 모든 이슈 정보를 가져오기는 아까워서 임시로 생성, 안만들어도 될거같기도하고....
class OnlyIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class IssueTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueTag
        fields = ('id', 'name')


class IssueLikeSerializer(serializers.ModelSerializer):

    #issue = OnlyIdSerializer(read_only=True)
    #user = NanumUserSerializer(read_only=True)

    class Meta:
        model = IssueLike
        fields = ('issue', 'user', 'create_date')


class IssueSerializer(serializers.ModelSerializer):

    tags = IssueTagSerializer(many=True)
    user = NanumUserSerializer(read_only=True)
    #likes = IssueLikeSerializer(many=True)

    class Meta:
        model = Issue
        fields = (
            'title', 'contents', 'count', 'comment_count', 'create_date', 'update_date',
            'like_count', 'thumbnail', 'user', 'tags'
        )

    # TODO 로그인,프론트 만들고서 다시 테스트
    def create(self, validated_data):
        # TODO 이슈 생성 시에 태그 같이 생성
        tags_data = validated_data.pop('tags')

        # TODO 로그인된 사용자 세션 입력으로 바꾸기
        validated_data['user_id'] = 1

        issue = Issue(**validated_data)
        for tag_data in tags_data:
            tag = IssueTag.objects.create(**tag_data)
            issue.tags.add(tag)
        issue.save()
        return issue

    # TODO 테스트 필요
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.contents = validated_data.get('contents', instance.contents)
        instance.thumbnail = validated_data.get('thumbnail', instance.thumbnail)
        instance.save()
        return instance


class IssueCommentSerializer(serializers.ModelSerializer):

    user = NanumUserSerializer(read_only=True)
    issue = OnlyIdSerializer(read_only=True)
    # issue = serializers.CharField()
    # __str__ return 값의 영향을 받음

    class Meta:
        model = IssueComment
        fields = ('id', 'contents', 'create_date', 'update_date', 'user', 'issue')

    # def create(self, validated_data):
    #     import logging
    #     logging.warning(validated_data)
    #     # TODO 이슈, 유저 연결하기
    #     #issue = get_object_or_404(Issue, pk=validated_data.pop('issue'))
    #     #user = validated_data.pop('user')
    #     comment = IssueComment(**validated_data)
    #     #comment.user.add(user)
    #     #comment.issue.add(issue)
    #     comment.save()
    #     return comment


class IssueFileSerializer(serializers.ModelSerializer):

    issue = OnlyIdSerializer(read_only=True)

    class Meta:
        model = IssueFile
        fields = ('id', 'name', 'size', 'download_count', 'create_date',
                  'update_date', 'attached_file', 'issue')




