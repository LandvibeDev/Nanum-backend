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

# /study/{pk}/board/{b_id}/calender/ :get, post
# /study/{pk}/board/{b_id}/calender/{c_pk}/ : get, put, patch, delete
calender_router = nested_routers.NestedSimpleRouter(board_router, r'board', lookup='board')
calender_router.register(r'calendar', CalendarViewSet, base_name='study-board-calendar')

# /study/{pk}/board/{b_id}/calender_tag/ :get, post
# /study/{pk}/board/{b_id}/calender_tag/{ct_pk}/ : get, put, patch, delete
calender_tag_router = nested_routers.NestedSimpleRouter(board_router, r'board', lookup='board')
calender_tag_router.register(r'calendar_tag', CalendarTagViewSet, base_name='study-board-calen  dar_tag')

# /study/{pk}/board/{b_id}/reference/ :get, post
# /study/{pk}/board/{b_id}/reference/{r_pk}/ : get, put, patch, delete
reference_router = nested_routers.NestedSimpleRouter(board_router, r'board', lookup='board')
reference_router.register(r'reference', ReferenceViewSet, base_name='study-board-reference')

# /study/{pk}/board/{b_id}/reference/{r_pk}/file/ :get, post
# /study/{pk}/board/{b_id}/reference/{r_pk}/file/{c_pk}/ : get, put, patch, delete
reference_file_router = nested_routers.NestedSimpleRouter(reference_router, r'reference', lookup='reference')
reference_file_router.register(r'file', ReferenceFileViewSet, base_name='study-board-reference-file')

# /study/{pk}/board/{b_id}/verification/ :get, post
# /study/{pk}/board/{b_id}/verification/{v_pk}/ : get, put, patch, delete
verification_router = nested_routers.NestedSimpleRouter(board_router, r'board', lookup='board')
verification_router.register(r'verification', VerificationViewSet, base_name='study-board-verification')

# /study/{pk}/board/{b_id}/verification/{r_pk}/file/ :get, post
# /study/{pk}/board/{b_id}/verification/{r_pk}/file/{c_pk}/ : get, put, patch, delete
verification_file_router = nested_routers.NestedSimpleRouter(verification_router, r'verification', lookup='verification')
verification_file_router.register(r'file', VerificationFileViewSet, base_name='study-board-verification-file')

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