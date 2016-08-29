from django.conf.urls import url, include

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from study.views import *

# /study :get, post
# /study/{pk} : get, put, patch, delete
study_router = nested_routers.DefaultRouter()
study_router.register(r'study', StudyViewSet, base_name='study')

# /study/{pk}/member/ :get, post
# /study/{pk}/member/{m_pk} : get, put, patch, delete
member_router = nested_routers.NestedSimpleRouter(study_router, r'study', lookup='study')
member_router.register(r'member', StudyMemberViewSet, base_name='study-member')

# /study/{pk}/board/ :get, post
# /study/{pk}/board/{n_pk} : get, put, patch, delete
board_router = nested_routers.NestedSimpleRouter(study_router, r'study', lookup='study')
board_router.register(r'board', BoardViewSet, base_name='study-board')

# like => function
# /study/{pk}/like : post
# /study/{pk}/like/{l_pk} : delete
# /study/{pk}/lastests =>function

urlpatterns = [
    # 여기 FBV의 url들을 추가
    url(r'^study/(?P<study_pk>[0-9]+)/like/$', study_like_create, name='like_create'),
    url(r'^study/(?P<study_pk>[0-9]+)/like/(?P<like_pk>[0-9]+)/$', study_like_delete, name='like_delete'),
    # url(r'^study/(?P<study_pk>[0-9]+)/lastest/$', lastest, name='lastest'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])