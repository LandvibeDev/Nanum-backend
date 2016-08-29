from django.conf.urls import url, include

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from reference.views import *
from study.urls import board_router

# /study/{pk}/board/{b_id}/reference/ :get, post
# /study/{pk}/board/{b_id}/reference/{r_pk}/ : get, put, patch, delete
reference_router = nested_routers.NestedSimpleRouter(board_router, r'board', lookup='board')
reference_router.register(r'reference', ReferenceViewSet, base_name='study-board-reference')

# /study/{pk}/board/{b_id}/reference/{r_pk}/file/ :get, post
# /study/{pk}/board/{b_id}/reference/{r_pk}/file/{c_pk}/ : get, put, patch, delete
reference_file_router = nested_routers.NestedSimpleRouter(reference_router, r'reference', lookup='reference')
reference_file_router.register(r'file', ReferenceFileViewSet, base_name='study-board-reference-file')
