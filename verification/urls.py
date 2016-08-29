from django.conf.urls import url, include

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from verification.views import *
from study.urls import board_router


# /study/{pk}/board/{b_id}/verification/ :get, post
# /study/{pk}/board/{b_id}/verification/{v_pk}/ : get, put, patch, delete
verification_router = nested_routers.NestedSimpleRouter(board_router, r'board', lookup='board')
verification_router.register(r'verification', VerificationViewSet, base_name='study-board-verification')

# /study/{pk}/board/{b_id}/verification/{r_pk}/file/ :get, post
# /study/{pk}/board/{b_id}/verification/{r_pk}/file/{c_pk}/ : get, put, patch, delete
verification_file_router = nested_routers.NestedSimpleRouter(verification_router, r'verification', lookup='verification')
verification_file_router.register(r'file', VerificationFileViewSet, base_name='study-board-verification-file')
