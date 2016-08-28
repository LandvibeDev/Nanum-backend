from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from study.urls import board_router
from homework.views import *


# /study/{pk}/homework :get, post
# /study/{pk}/homework/{h_pk} : get, put, patch, delete
homework_router = nested_routers.NestedSimpleRouter(board_router, r'board', lookup='board')
homework_router.register(r'homework', HomeWorkViewSet, base_name='board-homework')

# /study/{pk}/homework/{h_pk}/comment :get, post
# /study/{pk}/homework/{h_pk}/comment/{c_pk} : get, put, patch, delete
# comment_router = nested_routers.NestedSimpleRouter(homework_router, r'homework', lookup='homework')
# comment_router.register(r'comment', CommentViewSet, base_name='study-homework-comment')

# /study/{pk}/homework/{h_pk}/file :get, post
# /study/{pk}/homework/{h_pk}/file/{f_pk} : get, put, patch, delete
file_router = nested_routers.NestedSimpleRouter(homework_router, r'homework', lookup='homework')
file_router.register(r'file', HomeWorkFileViewSet, base_name='board-homework-file')

# /study/{pk}/homework/{h_pk}/submit :get, post
# /study/{pk}/homework/{h_pk}/submit/{s_pk} : get, put, patch, delete
# submit_router = nested_routers.NestedSimpleRouter(homework_router, r'homework', lookup='homework')
# submit_router.register(r'submit', SubmitViewSet, base_name='study-homework-submit')

# /study/{pk}/homework/{h_pk}/submit/{s_pk}/file :get, post
# /study/{pk}/homework/{h_pk}/submit/{s_pk}/file/{f_pk} : get, put, patch, delete
# submit_file_router = nested_routers.NestedSimpleRouter(submit_router, r'submit', lookup='submit')
# submit_file_router.register(r'file', SubmitFileViewSet, base_name='study-homework-submit-file')

# /study/{pk}/homework/{h_pk}/submit/{s_pk}/feedback :get, post
# /study/{pk}/homework/{h_pk}/submit/{s_pk}/feedback/{f_pk} : get, put, patch, delete
# submit_feedback_router = nested_routers.NestedSimpleRouter(submit_router, r'submit', lookup='submit')
# submit_feedback_router.register(r'feedback', FeedbackViewSet, base_name='study-homework-submit-feedback')
