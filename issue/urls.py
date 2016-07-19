from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from issue.views import *

# /issues/ : get, post
# /issues/{pk} : get, put, delete
issue_router = nested_routers.DefaultRouter()
issue_router.register(r'issues', IssueViewSet, base_name='issues')

# /issues/{pk}/comments : get, post
# /issues/{pk}/comments/{c_pk} : get, put, delete
comment_router = nested_routers.NestedSimpleRouter(issue_router, r'issues', lookup='issue')
comment_router.register(r'comments', CommentViewSet, base_name='issue-comments')

# /issues/{pk}/files : get, post
# /issues/{pk}/files/{f_pk} : get, put, delete
file_router = nested_routers.NestedSimpleRouter(issue_router, r'issues', lookup='issue')
file_router.register(r'files', FileViewSet, base_name='issue-files')

urlpatterns = format_suffix_patterns([
    url(r'^issues/(?P<issue_pk>[0-9]+)/tags/$', tag_create, name='tag_create'),
    url(r'^issues/(?P<issue_pk>[0-9]+)/tags/(?P<tag_pk>[0-9]+)/$', tag_delete, name='tag_delete'),
    url(r'^issues/(?P<issue_pk>[0-9]+)/likes/$', like_create, name='like_create'),
    url(r'^issues/(?P<issue_pk>[0-9]+)/likes/(?P<like_pk>[0-9]+)/$', like_delete, name='like_delete'),
])

# issue_list = IssueViewSet.as_view({
#     'get': 'list',
#     'post': 'create',
# })
#
# issue_detail = IssueViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy',
# })
