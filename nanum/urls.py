"""nanum URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth import views as account_views
from django.conf.urls.static import static
from django.shortcuts import redirect

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

from issue.urls import issue_router, comment_router, file_router
from issue.urls import urlpatterns as issue_urls
from study.urls import *
from homework.urls import *
from accounts.urls import *
from basic_board.urls import *
from reference.urls import *
from study.urls import urlpatterns as study_urls
from accounts.views import join, delete_account, info_account, first_page

from nanum.settings import base



urlpatterns = [
    # first page
    url(r'^$', first_page, name='main'),

    # admin
    url(r'^admin/', admin.site.urls),

    # before login, get token
    url(r'^obtain-auth-token/$', obtain_auth_token),
    url(r'^', include(user_router.urls), name='user'),
    # accounts
    url(
        r'^accounts/login/$', account_views.login, name='login',
        kwargs={
            'template_name': 'login.html'
        }
    ),
    url(r'^accounts/logout/$', account_views.logout, name='logout'),
    url(r'^accounts/join/$', join, name='join'),
    url(r'^accounts/delete/(?P<username>[\w]+)$', delete_account, name='delete'),
    url(r'^accounts/info/(?P<user_pk>[\w]+)$', info_account, name='info'),

    # study - study, board, member, like
    url(r'^', include(study_router.urls), name='study'),
    url(r'^', include(member_router.urls), name='study-member'),
    url(r'^', include(board_router.urls), name='study-board'),
    url(r'^', include(study_urls), name='study-urls'),

    # basic_board
    url(r'^', include(basic_board_router.urls), name='study-board-basic_board'),
    url(r'^', include(basic_board_comment_router.urls), name='study-board-basic_board-comment'),
    url(r'^', include(basic_board_file_router.urls), name='study-board-basic_board-file'),

    # reference
    url(r'^', include(reference_router.urls), name='study-reference'),
    url(r'^', include(reference_file_router.urls), name='study-reference-file'),

    # verification
    url(r'^', include(verification_router.urls), name='study-board-verification'),
    url(r'^', include(verification_file_router.urls), name='study-board-verification-file'),

    # calendar
    url(r'^', include(calender_router.urls), name='study-board-calender'),
    url(r'^', include(calender_tag_router.urls), name='study-board-calender_tag'),

    # homework
    url(r'^', include(homework_router.urls), name='homework'),
    url(r'^', include(file_router.urls), name='homework-file'),
    # url(r'^', include(comment_router.urls), name='homework-comment'),
    # url(r'^', include(submit_router.urls), name='homework-submit'),
    # url(r'^', include(submit_file_router.urls), name='homework-submit-file'),
    # url(r'^', include(submit_feedback_router.urls), name='homework-submit-feedback'),

    # # issue
    # url(r'^', include(issue_router.urls), name='issue'),
    # url(r'^', include(comment_router.urls), name='issue-comment'),
    # url(r'^', include(file_router.urls), name='issue-file'),
    # url(r'^', include(issue_urls), name='issue-tags'),
]

# using image url
urlpatterns += static(
    base.MEDIA_URL, document_root=base.MEDIA_ROOT
)