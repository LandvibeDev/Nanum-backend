from django.conf.urls import url, include

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from study.views import *

# /study :get, post
# /study/{pk} : get, put, patch, delete
study_router = nested_routers.DefaultRouter()
study_router.register(r'study', StudyViewSet, base_name='study')

# /study/{pk}/member :get, post
# /study/{pk}/member/{m_pk} : get, put, patch, delete
member_router = nested_routers.NestedSimpleRouter(study_router, r'study', lookup='study')
member_router.register(r'member', MemberViewSet, base_name='study-member')

# /study/{pk}/notice :get, post
# /study/{pk}/notice/{n_pk} : get, put, patch, delete
notice_router = nested_routers.NestedSimpleRouter(study_router, r'study', lookup='study')
notice_router.register(r'notice', NoticeViewSet, base_name='study-notice')

# /study/{pk}/calender :get, post
# /study/{pk}/calender/{c_pk} : get, put, patch, delete
calender_router = nested_routers.NestedSimpleRouter(study_router, r'study', lookup='study')
calender_router.register(r'calender', CalenderViewSet, base_name='study-calender')

# /study/{pk}/category/ :get, post
# /study/{pk}/category/{cc_pk} : get, put, patch, delete
calendertag_router = nested_routers.NestedSimpleRouter(study_router, r'study', lookup='study')
calendertag_router.register(r'calendertag', CalenderTagViewSet, base_name='study-calendertag')

# /study/{pk}/reference :get, post
# /study/{pk}/reference/{r_pk} : get, put, patch, delete
reference_router = nested_routers.NestedSimpleRouter(study_router, r'study', lookup='study')
reference_router.register(r'reference', ReferenceViewSet, base_name='study-reference')

# /study/{pk}/reference/{r_pk}/comment :get, post
# /study/{pk}/reference/{r_pk}/comment/{c_pk} : get, put, patch, delete
reference_comment_router = nested_routers.NestedSimpleRouter(reference_router, r'reference', lookup='reference')
reference_comment_router.register(r'comment', ReferenceCommentViewSet, base_name='study-reference-comment')

# /study/{pk}/reference/{r_pk}/file :get, post
# /study/{pk}/reference/{r_pk}/file/{c_pk} : get, put, patch, delete
reference_file_router = nested_routers.NestedSimpleRouter(reference_router, r'reference', lookup='reference')
reference_file_router.register(r'file', ReferenceFileViewSet, base_name='study-reference-file')

# /study/{pk}/question :get, post
# /study/{pk}/question/{q_pk} : get, put, patch, delete
question_router = nested_routers.NestedSimpleRouter(study_router, r'study', lookup='study')
question_router.register(r'question', QuestionViewSet, base_name='study-question')

# /study/{pk}/question/{q_pk}/comment :get, post
# /study/{pk}/question/{q_pk}/comment/{c_pk} : get, put, patch, delete
question_comment_router = nested_routers.NestedSimpleRouter(question_router, r'question', lookup='question')
question_comment_router.register(r'comment', QuestionCommentViewSet, base_name='study-question-comment')

# /study/{pk}/question/{q_pk}/file :get, post
# /study/{pk}/question/{q_pk}/file/{c_pk} : get, put, patch, delete
question_file_router = nested_routers.NestedSimpleRouter(question_router, r'question', lookup='question')
question_file_router.register(r'file', QuestionFileViewSet, base_name='study-question-file')

# like => function
# /study/{pk}/like : post
# /study/{pk}/like/{l_pk} : delete
# /study/{pk}/lastests =>function

urlpatterns = [
    # 여기 FBV의 url들을 추가
    url(r'^study/(?P<study_pk>[0-9]+)/like/$', like_create, name='like_create'),
    url(r'^study/(?P<study_pk>[0-9]+)/like/(?P<like_pk>[0-9]+)/$', like_delete, name='like_delete'),
    url(r'^study/(?P<study_pk>[0-9]+)/lastest/$', lastest, name='lastest'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])