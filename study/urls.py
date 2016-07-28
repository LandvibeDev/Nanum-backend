from django.conf.urls import url

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

# /study/{pk}/calender :get, post
# /study/{pk}/calender/{c_pk} : get, put, patch, delete
calender_router = nested_routers.NestedSimpleRouter(study_router, r'study', lookup='study')
calender_router.register(r'calender', CalenderViewSet, base_name='study-calender')

# /study/{pk}/reference :get, post
# /study/{pk}/reference/{r_pk} : get, put, patch, delete
reference_router = nested_routers.NestedSimpleRouter(study_router, r'study', lookup='study')
reference_router.register(r'reference', ReferenceViewSet, base_name='study-reference')

# /study/{pk}/reference :get, post
# /study/{pk}/reference/{r_pk} : get, put, patch, delete
reference_router = nested_routers.NestedSimpleRouter(study_router, r'study', lookup='study')
reference_router.register(r'reference', ReferenceViewSet, base_name='study-reference')

# /study/{pk}/reference/{r_pk}/comment :get, post
# /study/{pk}/reference/{r_pk}/comment/{c_pk} : get, put, patch, delete
reference_comment_router = nested_routers.NestedSimpleRouter(reference_router, r'reference', lookup='reference')
reference_comment_router.register(r'comment',ReferenceCommentViewSet, base_name='study-reference-comment')

# /study/{pk}/reference/{r_pk}/file :get, post
# /study/{pk}/reference/{r_pk}/file/{c_pk} : get, put, patch, delete
reference_file_router = nested_routers.NestedSimpleRouter(reference_router, r'reference', lookup='reference')
reference_file_router.register(r'file',ReferenceFileViewSet, base_name='study-reference-file')

# /study/{pk}/question :get, post
# /study/{pk}/question/{q_pk} : get, put, patch, delete
question_router = nested_routers.NestedSimpleRouter(study_router, r'study', lookup='study')
question_router.register(r'question', QuestionViewSet, base_name='study-question')

# /study/{pk}/question/{q_pk}/comment :get, post
# /study/{pk}/question/{q_pk}/comment/{c_pk} : get, put, patch, delete
question_comment_router = nested_routers.NestedSimpleRouter(reference_router, r'question', lookup='question')
question_comment_router.register(r'comment', QuestionCommentViewSet, base_name='study-question-comment')

# /study/{pk}/question/{q_pk}/file :get, post
# /study/{pk}/question/{q_pk}/file/{c_pk} : get, put, patch, delete
question_file_router = nested_routers.NestedSimpleRouter(reference_router, r'question', lookup='question')
question_file_router.register(r'file', QuestionFileViewSet, base_name='study-question-file')

# like => function
# /study/{pk}/lastests =>function
