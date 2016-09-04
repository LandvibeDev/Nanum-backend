from django.conf.urls import url, include

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from basic_board.views import *
from study.urls import board_router

# /study/{pk}/board/{b_id}/basic_board/ :get, post
# /study/{pk}/board/{b_id}/basic_board/{bb_pk}/ : get, put, patch, delete
basic_board_router = nested_routers.NestedSimpleRouter(board_router, r'board', lookup='board')
basic_board_router.register(r'basic_board', BasicBoardViewSet, base_name='study-board-basic_board')

# /study/{pk}/board/{b_id}/basic_board/{bb_pk}/comment :get, post
# /study/{pk}/board/{b_id}/basic_board/{bb_pk}/comment/{c_pk} : get, put, patch, delete
basic_board_comment_router = nested_routers.NestedSimpleRouter(basic_board_router, r'basic_board', lookup='basic_board')
basic_board_comment_router.register(r'comment', BasicBoardCommentViewSet, base_name='study-board-basic_board-comment')

# /study/{pk}/board/{b_id}/basic_board/{bb_pk}/comment :get, post
# /study/{pk}/board/{b_id}/basic_board/{bb_pk}/comment/{c_pk} : get, put, patch, delete
basic_board_file_router = nested_routers.NestedSimpleRouter(basic_board_router, r'basic_board', lookup='basic_board')
basic_board_file_router.register(r'file', BasicBoardFileViewSet, base_name='study-board-basic_board-file')

urlpatterns = [
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])