from django.conf.urls import url, include

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from schedule.views import *
from study.urls import board_router


# /study/{pk}/board/{b_id}/schedule/ :get, post
# /study/{pk}/board/{b_id}/schedule/{c_pk}/ : get, put, patch, delete
schedule_router = nested_routers.NestedSimpleRouter(board_router, r'board', lookup='board')
schedule_router.register(r'schedule', ScheduleViewSet, base_name='study-board-schedule')

# /study/{pk}/board/{b_id}/schedule_tag/ :get, post
# /study/{pk}/board/{b_id}/schedule_tag/{ct_pk}/ : get, put, patch, delete
schedule_tag_router = nested_routers.NestedSimpleRouter(board_router, r'board', lookup='board')
schedule_tag_router.register(r'schedule_tag', ScheduleTagViewSet, base_name='study-board-schedule_tag')
