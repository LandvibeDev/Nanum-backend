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
import rest_framework

from issue.urls import issue_router, comment_router, file_router
from issue.urls import urlpatterns as issue_urls
from study.urls import *
from homework.urls import *
from study.urls import urlpatterns as study_urls
from accounts.views import join, delete_account, info_account, first_page
from nanum.settings import base



urlpatterns = [
    # first page
    url(r'^$', first_page, name='main'),

    # admin
    url(r'^admin/', admin.site.urls),

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


    #study
    url(r'^', include(study_router.urls), name='study'),
    url(r'^', include(member_router.urls), name='study-memeber'),
    url(r'^', include(notice_router.urls), name='study-notice'),
    url(r'^', include(calender_router.urls), name='study-calender'),
    url(r'^', include(calendertag_router.urls), name='study-calendertag'),
    url(r'^', include(reference_router.urls), name='study-reference'),
    url(r'^', include(reference_comment_router.urls), name='study-reference-commnet'),
    url(r'^', include(reference_file_router.urls), name='study-reference-file'),
    url(r'^', include(question_router.urls), name='study-question'),
    url(r'^', include(question_comment_router.urls), name='study-question-comment'),
    url(r'^', include(question_file_router.urls), name='study-question-file'),
    url(r'^', include(study_urls), name='study-urls'),


    # homework
    url(r'^', include(homework_router.urls), name='homework'),
    url(r'^', include(comment_router.urls), name='homework-comment'),
    url(r'^', include(file_router.urls), name='homework-file'),
    url(r'^', include(submit_router.urls), name='homework-submit'),
    url(r'^', include(submit_file_router.urls), name='homework-submit-file'),
    url(r'^', include(submit_feedback_router.urls), name='homework-submit-feedback'),

    # issue
    url(r'^', include(issue_router.urls), name='issue'),
    url(r'^', include(comment_router.urls), name='issue-comment'),
    url(r'^', include(file_router.urls), name='issue-file'),
    url(r'^', include(issue_urls), name='issue-tags'),


]

# using image url
urlpatterns += static(
    base.MEDIA_URL, document_root=base.MEDIA_ROOT
)