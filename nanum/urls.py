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

from rest_framework.urlpatterns import format_suffix_patterns

from issue.urls import issue_router, comment_router, file_router
from issue.urls import urlpatterns as issue_urls
from study.urls import *
from study.urls import urlpatterns as study_urls

from accounts.views import join, delete_account
from nanum.settings import base

urlpatterns = [

    #admin
    url(r'^admin/', admin.site.urls),

    #account
    url(
        r'^accounts/login/$', account_views.login, name='login',
        kwargs={
            'template_name': 'login.html'
        }
    ),
    url(r'^accounts/logout/$', account_views.logout, name='logout'),
    url(r'^accounts/join/$', join, name='join'),
    url(r'^accounts/delete/(?P<username>[\w]+)$', delete_account, name='delete'),


    #study
    url(r'^', include(study_router.urls), name='study'),
    url(r'^', include(member_router.urls), name='study-memeber'),
    url(r'^', include(notice_router.urls), name='study-notice'),
    url(r'^', include(calender_router.urls), name='study-calender'),
    url(r'^', include(reference_router.urls), name='study-reference'),
    url(r'^', include(reference_comment_router.urls), name='study-reference-commnet'),
    url(r'^', include(reference_file_router.urls), name='study-reference-file'),
    url(r'^', include(question_router.urls), name='study-question'),
    url(r'^', include(question_comment_router.urls), name='study-question-comment'),
    url(r'^', include(question_file_router.urls), name='study-question-file'),


    #homework url 추가할 것


    #issue
    url(r'^', include(issue_router.urls), name='issue'),
    url(r'^', include(comment_router.urls), name='issue-comment'),
    url(r'^', include(file_router.urls), name='issue-file'),
    url(r'^', include(issue_urls), name='issue-tags'),

]

# using image url
urlpatterns += static(
    base.MEDIA_URL, document_root=base.MEDIA_ROOT
)