from django.contrib.auth.models import Permission, Group

from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.decorators import api_view, permission_classes

from study.models import *


# 스터디 모델 생성 되면 구현 완료할 것!
# 권한 관련 레퍼런스
# http://www.django-rest-framework.org/api-guide/permissions/#custom-permissions

# TODO 테스트 필요
class WriterPermission(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user

# # TODO 테스트 필요
# class StudyMemeberPermission(BasePermission):
#     """
#     Allows access to authenticated users and study memebers.
#     """
#     def has_permission(self, request, view):
#         if getattr(view, '_ignore_model_permissions', False):
#             return True
#
#         if hasattr(view, 'get_queryset'):
#             queryset = view.get_queryset()
#         else:
#             queryset = getattr(view, 'queryset', None)
#
#         assert queryset is not None, (
#             'Cannot apply ModifiedPermission on a view that '
#             'does not set `.queryset` or have a `.get_queryset()` method.'
#         )
#
#         req_user_study_list = Member.objects.filter(user__pk=request.user.pk)
#
#         for member in req_user_study_list:
#             if member.study == queryset.study.id and request.user and request.user.is_authenticated():
#                 return True
#
#         return False

# TODO 테스트 필요
class StudyMemeberPermission(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        request_joined_studies = Member.objects.filter(user=request.user)
        return obj.study in request_joined_studies


# 스터디장, 스터디 매니저, 스터디원 그룹 생성)
def create_groups(study_name, leader, manager_list=None, member_list=None):
    # 스터디 존재 제크
    try:
        study = Study.objects.filter(name=study_name)
    except Study.DoesNotExist:
        return

    # 그룹 3개 생성
    leader = Group(name=study_name + '_leader')
    managers = Group(name=study_name + '_managers')
    members = Group(name=study_name + '_members')

    # 권한 생성
    """
    content_type = {
        "id" : 99????,
        "app_label" : "study",
        "model" : "study_permission"
        }
    """
    add_p = Permission.objects.create(
        name="Can add " + study_name,
        #content_type=99,
        codename="add_"+study_name
    )
    get_p = Permission.objects.create(
        name="Can get " + study_name,
        # content_type=99,
        codename="get_" + study_name
    )

    change_p = Permission.objects.create(
        name="Can change" + study_name,
        # content_type=99,
        codename="change_" + study_name
    )
    delete_p = Permission.objects.create(
        name="Can delete" + study_name,
        # content_type=99,
        codename="delete_" + study_name
    )
    # manager, user 추가/삭제 권한

    # 해당 그룹에 맞는 권한 저장
    leader.permissions.add(add_p, get_p, change_p, delete_p)
    managers.permissions.add(add_p, get_p, change_p, delete_p)
    members.permissions(add_p, get_p)

    # 입력받은 사용자를 그룹에 추가 (reverse MtoM)
    leader.user_set.add(leader)
    for m in manager_list:
        managers.user_set.add(m)
    for m in member_list:
        members.user_set.add(m)

    leader.save()
    managers.save()
    members.save()


def add_managers_to_group(manager_list):
    pass


def add_users_to_group(user_list):
    pass


def delete_users_from_group(user_list):
    pass


def delete_managers_from_group(user_list):
    pass


def change_leader(leader):
    pass
