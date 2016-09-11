from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from logging import warning

from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView

import logging

from basic_board.models import *
from basic_board.serializer import *
from accounts.serializer import *


# ===================================================
# ============== type 0 : BasicBoard ==============
# ===================================================
@permission_classes((AllowAny,))
class BasicBoardViewSet(viewsets.ModelViewSet):
    """
    create - request copy 인스턴스에 __setitem__('key', value) 함수로 url에 포함된 pk값 반영
    retrieve, list, update, destroy - queryset.filter 로 url 에 포함된 pk값 반영

    create - 한단계 상위 모델의 pk만 반영
    retrieve, list - 모든 단계의 상위 모델의 pk 반영
    update, destroy 는 filter 를 적용안해도 될거같은데 일단 BasicBoardViewSet만 적용해봄

    kwargs 로 url 에 있는 pk 값들이 넘어오므로 request body 에 값을 넣을 필요가 없다.
    단, url 에 없는 pk 값은 request body 에 포함. user_pk
    """
    queryset = BasicBoard.objects.all()
    # get 시리얼라이저
    serializer_class = BasicBoardGetSerializer

    # override GenericAPIView.get_serializer
    def _get_serializer(self, *args, **kwargs):
        # create, update 시리얼라이저
        serializer_class = BasicBoardSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # override ModelViewSet.CreateModelMixin.create
    def create(self, request, *args, **kwargs):
        """
        user pk 값은 reqeust body 로 넘겨줄 필요가 있다.
        :param request: user, BasicBoard 필드
        :param args: x
        :param kwargs: board_pk, study_pk
        :return:
        """
        # 수정가능한 request 얻기
        request_copy = request.POST.copy()
        # request copy 에 인자 추가
        request_copy.__setitem__('board', kwargs.get('board_pk'))
        serializer = self._get_serializer(data=request_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # override
    def retrieve(self, request, *args, **kwargs):
        """
        url 깊이가 깊어질수록 study/{s_id}/board/{b_id}/basic_board/{bb_id}/~
        kwargs 의 인자로 포함되어 넘어오는 pk 값이 많아진다. 이를 활용하여 retrieve 함수를 오버라이딩
        모든 뷰함수에 적용됨
        :param request: x
        :param args: x
        :param kwargs: pk, board_pk, study_pk
        :return:
        """
        """
        BasicBoard 의 필드에는 board 만 있다.
        그런데 board 부터 언더바(_) 두개를 붙이면 board 의 상위 모델인 study 까지 참조가 가능하다.
        """
        queryset = self.queryset.filter(pk=kwargs.get('pk'),
                                        board=kwargs.get('board_pk'),
                                        board__study=kwargs.get('study_pk'))
        """
        https://github.com/alanjds/drf-nested-routers
        여기서는 get_object_or_404 의 인자로 pk 까지 넘겨준다. 안넘겨줘도 결과는 똑같다. 왜 넣었을까
        """
        instance = get_object_or_404(queryset, pk=kwargs.get('pk'))
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # override ModelViewSet.UpdateModelMixin.update
    def update(self, request, *args, **kwargs):
        """
        :param request: BasicBoard 필드
        :param args: x
        :param kwargs: pk, board_pk, study_pk
        :return:
        """
        partial = kwargs.pop('partial', False)
        # 주어진 인자에 만족하는 BasicBoard 인스턴스 정보 변경
        queryset = self.queryset.filter(pk=kwargs.get('pk'),
                                        board=kwargs.get('board_pk'),
                                        board__study=kwargs.get('study_pk'))
        instance = get_object_or_404(queryset, pk=kwargs.get('pk'))
        serializer = self._get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # override
    def list(self, request, *args, **kwargs):
        """
        :param request: x
        :param args: x
        :param kwargs: board_pk, study_pk
        :return:
        """
        # 주어진 인자에 만족하는 BasicBoard 리스트 반환
        queryset = self.queryset.filter(board=kwargs.get('board_pk'),
                                        board__study=kwargs.get('study_pk'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # override
    def destroy(self, request, *args, **kwargs):
        """
        :param request: x
        :param args: x
        :param kwargs: pk, board_pk, study_pk
        :return:
        """
        # 주어진 인자에 만족하는 BasicBoard 인스턴스 삭제
        queryset = self.queryset.filter(pk=kwargs.get('pk'),
                                        board=kwargs.get('board_pk'),
                                        board__study=kwargs.get('study_pk'))
        instance = get_object_or_404(queryset, pk=kwargs.get('pk'))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)



@permission_classes((AllowAny,))
class BasicBoardCommentViewSet(viewsets.ModelViewSet):
    queryset = BasicBoardComment.objects.all()
    serializer_class = BasicBoardGetCommentGetSerializer

    # override GenericAPIView.get_serializer
    def _get_serializer(self, *args, **kwargs):
        serializer_class = BasicBoardCommentSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # override ModelViewSet.CreateModelMixin.create
    def create(self, request, *args, **kwargs):
        """
        user pk 값은 reqeust body 로 넘겨줄 필요가 있다.
        :param request: user, BasicBoard 필드
        :param args: x
        :param kwargs: board_pk, study_pk
        :return:
        """
        # 수정가능한 request 얻기
        request_copy = request.POST.copy()
        # request copy 에 인자 추가
        request_copy.__setitem__('basic_board', kwargs.get('basic_board_pk'))
        serializer = self._get_serializer(data=request_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # override
    def retrieve(self, request, *args, **kwargs):
        """
        :param request: x
        :param args: x
        :param kwargs: pk, basic_board_pk, board_pk, study_pk
        :return:
        """
        """
        BasicBoardComment 의 필드에는 basic_board 만 있다.
        그런데 basic_board 부터 언더바(_) 두개를 붙이면 basic_board 의 상위 모델인 board, study pk 반영 가능.
        """
        queryset = self.queryset.filter(pk=kwargs.get('pk'),
                                        basic_board=kwargs.get('basic_board_pk'),
                                        basic_board__board=kwargs.get('board_pk'),
                                        basic_board__board__study=kwargs.get('study_pk'))
        # 해당 인자에 만족하는 BasicBoardComment 인스턴스 반환
        instance = get_object_or_404(queryset, pk=kwargs.get('pk'))
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # override ModelViewSet.UpdateModelMixin.update
    def update(self, request, *args, **kwargs):
        """
        :param request: BasicBoardComment 필드
        :param args: x
        :param kwargs: pk, basic_board_pk, board_pk, study_pk
        :return:
        """
        partial = kwargs.pop('partial', False)  #
        instance = self.get_object()
        serializer = self._get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # override
    def list(self, request, *args, **kwargs):
        """
        :param request: x
        :param args: x
        :param kwargs: basic_board_pk, board_pk, study_pk
        :return:
        """
        logging.warning('kwargs : ' + str(kwargs))
        # 주어진 인자에 만족하는 BasicBoardComment 리스트 반환
        queryset = self.queryset.filter(basic_board=kwargs.get('basic_board_pk'),
                                        basic_board__board=kwargs.get('board_pk'),
                                        basic_board__board__study=kwargs.get('study_pk'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@permission_classes((AllowAny,))
class BasicBoardFileViewSet(viewsets.ModelViewSet):
    queryset = BasicBoardFile.objects.all()
    serializer_class = BasicBoardFileGetSerializer

    def _get_serializer(self, *args, **kwargs):
        # serializer_class = self.get_serializer_class()
        serializer_class = BasicBoardFileSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # override ModelViewSet.CreateModelMixin.create
    def create(self, request, *args, **kwargs):
        """
        user pk 값은 reqeust body 로 넘겨줄 필요가 있다.
        :param request: user, BasicBoard 필드
        :param args: x
        :param kwargs: board_pk, study_pk
        :return:
        """
        # 수정가능한 request 얻기
        request_copy = request.POST.copy()
        # request copy 에 인자 추가
        request_copy.__setitem__('basic_board', kwargs.get('basic_board_pk'))
        serializer = self._get_serializer(data=request_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # override
    def retrieve(self, request, *args, **kwargs):
        """
        :param request: x
        :param args: x
        :param kwargs: pk, basic_board_pk, board_pk, study_pk
        :return:
        """
        """
        BasicBoardFile 의 필드에는 basic_board 만 있다.
        그런데 basic_board 부터 언더바(_) 두개를 붙이면 basic_board 의 상위 모델인 board, study pk 반영 가능.
        """
        queryset = self.queryset.filter(pk=kwargs.get('pk'),
                                        basic_board=kwargs.get('basic_board_pk'),
                                        basic_board__board=kwargs.get('board_pk'),
                                        basic_board__board__study=kwargs.get('study_pk'))
        # 해당 인자에 만족하는 BasicBoardFile 인스턴스 반환
        instance = get_object_or_404(queryset, pk=kwargs.get('pk'))
        # 다운로드 수 증가 및 적용
        instance.download_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # override
    def update(self, request, *args, **kwargs):
        """
        :param request: BasicBoardFile 필드
        :param args: x
        :param kwargs: pk, basic_board_pk, board_pk, study_pk
        :return:
        """
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        logging.warning('request :' + str(request.POST))

        """
        프론트에서 수정 시 어차피 attached_file 도 넘어오므로 그냥 삭제하고 다시 만들자.
        같은 파일일 시 그대로 놔두고, 다른 파일일 시 기존 파일 삭제하고 새로 반영하는 코드는 나중에
        """
        instance.attached_file.delete()  # 실제 file 삭제

        serializer = self._get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # override
    def list(self, request, *args, **kwargs):
        """
        :param request: x
        :param args: x
        :param kwargs: basic_board_pk, board_pk, study_pk
        :return:
        """
        # 주어진 인자에 만족하는 BasicBoardFile 리스트 반환
        queryset = self.queryset.filter(basic_board=kwargs.get('basic_board_pk'),
                                        basic_board__board=kwargs.get('board_pk'),
                                        basic_board__board__study=kwargs.get('study_pk'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # override
    def destroy(self, request, *args, **kwargs):
        """
        :param request: x
        :param args: x
        :param kwargs: pk, basic_board_pk, board_pk, study_pk
        :return:
        """
        instance = self.get_object()     # file 관련 인스턴스 개체 삭제
        instance.attached_file.delete()  # 실제 file 삭제
        return super(BasicBoardFileViewSet, self).destroy(request, *args, **kwargs)

